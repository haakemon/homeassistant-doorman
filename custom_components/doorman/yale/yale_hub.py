import logging
import requests
from custom_components.doorman.yale.expiration_data import ExpirationData, UpdateWrapper
from custom_components.doorman.yale.exceptions import LoginException, HttpResponseException, YaleHubStatusException
from custom_components.doorman.yale.device_factory import DeviceFactory

from datetime import datetime

class YaleHub:
    def __init__(self, username, password, zone_id):
        self._LOGGER = logging.getLogger(__name__)

        self.username = username
        self.password = password
        self.zone_id = zone_id

        self.token = UpdateWrapper(None, update_fn=self.get_access_token)
        self.state_data = UpdateWrapper(None, update_fn=self.get_state_data)
        self.state_history = UpdateWrapper(None, update_fn=self.get_state_history_data)

        self.devices = []

    def check_login_response(self, login_data):
        self._LOGGER.debug("check_login_response")
        if "error" in login_data:
            err_msg = login_data["error_description"]
            error_text = f"Login failed due to: {err_msg}"
            self._LOGGER.error(error_text)
            raise LoginException(error_text)

    def get_access_token(self) -> ExpirationData:
        self._LOGGER.debug("get_access_token")
        login_data = self.login()
        self.check_login_response(login_data)
        token = ExpirationData(
            login_data["access_token"],
            login_data["expires_in"],
            None)

        if token.is_active is False:
            raise LoginException("No valid token found")

        return token

    def extract_json(self, response):
        self._LOGGER.debug("Extract json")
        json = response.json()
        status = json["message"]
        if status != "OK!":
            error_text = f"Status is not OK!: {status}"
            self._LOGGER.error(error_text)
            raise YaleHubStatusException(error_text)
        return json.get("data")

    def get_state_data(self) -> ExpirationData:
        self._LOGGER.debug("get_state_data")
        response = requests.get(
            YaleApi.STATE_URL,
            headers=self.get_token_auth_header(),
            timeout=5)
        self.check_http_response(response)
        json = self.extract_json(response)
        data = ExpirationData(json, 10, None)
        return data

    def get_state_history_data(self) -> ExpirationData:
        self._LOGGER.debug("get_state_history_data")
        response = requests.get(
            YaleApi.STATE_HISTORY_URL,
            data={"page_num": 1, "set_utc": 1},
            headers=self.get_token_auth_header(),
            timeout=5)
        self.check_http_response(response)
        json = self.extract_json(response)
        data = ExpirationData(json, 10, None)
        return data

    def add_devices(self):
        self._LOGGER.debug("add_devices")
        data = self.state_data.data

        devices = data.get("device_status")
        for device in devices:
            device_id = device.get("device_id")
            name = device.get("name")
            device_type = device.get("type")
            yale_device = DeviceFactory(self, device_id, device_type, name)
            self._LOGGER.info(f"Adding device {name}")
            self.devices.append(yale_device)

    def update_state(self):
        data = self.state_data.data

        devices = data.get("device_status")
        for device in devices:
            device_id = device.get("device_id")
            device = [i for i in self.devices if i.device_id == device_id][0]
            device.state = device.get("status_open")[0]
            self._LOGGER.info(f"Device {device.name} updated, setting status to {device.state}")

    def setup_platform(self):
        """Set up the Doorman platform."""
        self._LOGGER.info("Setting up Doorman platform")
        self.add_devices()
        self.update_state()
