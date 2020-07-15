import logging
import requests
from custom_components.doorman.yale.expiration_data import ExpirationData, UpdateWrapper
from custom_components.doorman.yale.exceptions import LoginException, HttpResponseException, YaleHubStatusException
from custom_components.doorman.yale.device_factory import DeviceFactory

from custom_components.doorman.log.log_wrapper import logger

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

    def jsonify(func):
        def inner(*args, **kwargs):
            try:
                response = func(*args, **kwargs)
                return response.json()
            except Exception as error:
                raise Exception(f"Failed to convert to jason, {error}")
        return inner

    def check_http_response(func):
        def inner(response: requests.Response) -> requests.Response:
            if response.status_code != 200:
                error_text = f"Error retrieving http response: {response.text}"
                raise HttpResponseException(error_text)
            else:
                return response
        return inner

    def get_token_auth_header(token):
        return {"Authorization": f"Bearer {token}"}

    @check_http_response
    @jsonify
    @logger
    def login(username, password) -> requests.Request:
        headers = {"Accept": "application/json", "Authorization": f"Basic {YaleApi.YALE_AUTH_TOKEN}"}
        auth_data = {"grant_type": "password", "username": username, "password": password}
        response = requests.post(
            YaleApi.LOGIN_URL,
            data=auth_data,
            headers=headers)
        return response

    @check_http_response
    @jsonify
    @logger
    def get_state_data(token) -> requests.Request:
        response = requests.get(
            YaleApi.STATE_URL,
            headers=YaleApi.get_token_auth_header(token),
            timeout=5)
        return response

    @check_http_response
    @jsonify
    @logger
    def get_state_history_data(token) -> requests.Request:
        response = requests.get(
            YaleApi.STATE_HISTORY_URL,
            data={"page_num": 1, "set_utc": 1},
            headers=YaleApi.get_token_auth_header(token),
            timeout=5)
        return response

    @check_http_response
    @jsonify
    @logger
    def unlock(token, pincode):
        # area=1&zone=1&pincode=xxxxxxxx
        response = requests.get(
            YaleApi.DOOR_UNLOCK,
            data={"area": 1, "zone": 1, "pincode": pincode},
            headers=YaleApi.get_token_auth_header(token),
            timeout=5)
        return response

    @check_http_response
    @jsonify
    @logger
    def lock(token, device_id):
        # area=1&zone=1&device_sid=RF%3Axxxxxxxx&device_type=device_type.door_lock&request_value=1
        response = requests.get(
            YaleApi.DOOR_LOCK,
            data={"area": 1, "zone": 1, "device_sid": device_id, "device_type": "device_type.door_lock", "request_value": 1},
            headers=YaleApi.get_token_auth_header(token),
            timeout=5)
        return response
