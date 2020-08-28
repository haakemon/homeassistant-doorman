import logging
import requests

from custom_components.doorman.log.log_wrapper import logger
from custom_components.doorman.yale.exceptions import HttpResponseException, LoginException, UpdateException
from custom_components.doorman.yale.updateable import Updateable


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

        self.token = Token(self)

    @logger
    def login(self):
        return self.post(
            self.LOGIN_URL,
            data={"grant_type": "password", "username": self.username, "password": self.password},
            headers={"Accept": "application/json", "Authorization": f"Basic {self.YALE_AUTH_TOKEN}"})

    # @logger
    def get_state_data(self):
        json_message = self.get(
            self.STATE_URL,
            data="",
            headers=YaleApi.get_token_auth_header(self.token.data))
        return self.extract_message(json_message)

    # @logger
    def get_state_history_data(self):
        json_message = self.get(
            self.STATE_HISTORY_URL,
            data={"page_num": 1, "set_utc": 1},
            headers=YaleApi.get_token_auth_header(self.token.data))
        return self.extract_message(json_message)

    # @logger
    def unlock(self, area, zone, pincode):
        # area=1&zone=1&pincode=xxxxxxxx
        return self.post(
            self.DOOR_UNLOCK,
            data={"area": area, "zone": zone, "pincode": pincode},
            headers=YaleApi.get_token_auth_header(self.token.data),)

    # @logger
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
            raise LoginException(f"Invalid credentials given: {response.text}")
        else:
            raise HttpResponseException(f"Unknown error retrieving http response: {response.text}")

    def jsonify(self, response: requests.Response):
        try:
            json = response.json()
            return json
        except Exception as error:
            raise Exception(f"Failed to convert to jason, {error}")

    def extract_message(self, json):
        status = json["message"]
        if status != "OK!":
            raise Exception(f"Status is not OK: {status}")
        return json.get("data")

    def get_token_auth_header(token):
        return {"Authorization": f"Bearer {token}"}


class Token(Updateable):
    def __init__(self, yale_api):
        super().__init__(None, -1)

        self.yale_api = yale_api

    def update(self):
        login_json = self.yale_api.login()
        token = login_json["access_token"]
        self.time_valid = login_json["expires_in"]
        return token
