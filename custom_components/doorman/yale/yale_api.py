import logging
import requests

from custom_components.doorman.log.log_wrapper import logger
from custom_components.doorman.yale.exceptions import HttpResponseException, LoginException
from custom_components.doorman.yale.expiration_wrapper import ExpirationWrapper
from custom_components.doorman.yale.update_wrapper import UpdateWrapper

from datetime import datetime

class YaleApi:
    BASE_URL = "https://mob.yalehomesystem.co.uk/yapi"

    LOGIN_URL = BASE_URL + "/o/token/"
    STATE_URL = BASE_URL + "/api/panel/cycle/"
    STATE_HISTORY_URL = BASE_URL + "/api/event/report/?page_num=1&set_utc=1"

    DOOR_UNLOCK = BASE_URL + "/api/minigw/unlock/"
    DOOR_LOCK = BASE_URL + "/api/panel/device_control/"

    YALE_AUTH_TOKEN = 'VnVWWDZYVjlXSUNzVHJhcUVpdVNCUHBwZ3ZPakxUeXNsRU1LUHBjdTpkd3RPbE15WEtENUJ5ZW1GWHV0am55eGhrc0U3V0ZFY2p0dFcyOXRaSWNuWHlSWHFsWVBEZ1BSZE1xczF4R3VwVTlxa1o4UE5ubGlQanY5Z2hBZFFtMHpsM0h4V3dlS0ZBcGZzakpMcW1GMm1HR1lXRlpad01MRkw3MGR0bmNndQ=='

    _LOGGER = logging.getLogger(__name__)

    def __init__(self, username, password):
        self.username = username
        self.password = password

        self.token = UpdateWrapper(self.get_token(), update_fn=self.get_token, access_fn=lambda x: x.data)

    @logger
    def login(self):
        return self.post(
            self.LOGIN_URL,
            data={"grant_type": "password", "username": self.username, "password": self.password},
            headers={"Accept": "application/json", "Authorization": f"Basic {self.YALE_AUTH_TOKEN}"})

    @logger
    def get_state_data(self):
        return self.get(
            self.STATE_URL,
            data="",
            headers=YaleApi.get_token_auth_header(self.token.data))

    @logger
    def get_state_history_data(self):
        return self.get(
            self.STATE_HISTORY_URL,
            data={"page_num": 1, "set_utc": 1},
            headers=YaleApi.get_token_auth_header(self.token.data))

    @logger
    def unlock(self, area, zone, pincode):
        # area=1&zone=1&pincode=xxxxxxxx
        return self.post(
            self.DOOR_UNLOCK,
            data={"area": area, "zone": zone, "pincode": pincode},
            headers=YaleApi.get_token_auth_header(self.token.data),)

    @logger
    def lock(self, area, zone):
        # area=1&zone=1&device_type=device_type.door_lock&request_value=1
        return requests.post(
            self.DOOR_LOCK,
            data={"area": area, "zone": zone, "device_type": "device_type.door_lock", "request_value": 1},
            headers=YaleApi.get_token_auth_header(self.token.data))

    def post(self, url, data, headers):
        response = requests.post(url, data=data, headers=headers)
        self.check_http_response(response)
        json = self.jsonify(response)
        return json

    def get(self, url, data, headers):
        response = requests.get(url, data=data, headers=headers, timeout=5)
        self.check_http_response(response)
        json = self.jsonify(response)
        return json

    def check_http_response(self, response: requests.Response) -> requests.Response:
        if response.status_code == 200:
            return
        elif response.status_code == 401:
            error_text = f"Invalid credentials given: {response.text}"
            raise LoginException(error_text)
        else:
            error_text = f"Unknown error retrieving http response: {response.text}"
            raise HttpResponseException(error_text)

    def jsonify(self, response: requests.Response):
        try:
            json = response.json()
            return json
        except Exception as error:
            raise Exception(f"Failed to convert to jason, {error}")

    def get_token_auth_header(token):
        return {"Authorization": f"Bearer {token}"}

    def get_token(self) -> ExpirationWrapper:
        self._LOGGER.debug("get_access_token")
        login_json = self.login()

        token_data = ExpirationWrapper(
            login_json["access_token"],
            login_json["expires_in"])
        return token_data
