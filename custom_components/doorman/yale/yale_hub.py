import logging
import requests
from custom_components.doorman.yale.expiration_wrapper import ExpirationWrapper
from custom_components.doorman.yale.update_wrapper import UpdateWrapper
from custom_components.doorman.yale.exceptions import LoginException, HttpResponseException, YaleHubStatusException
from custom_components.doorman.yale.device_factory import DeviceFactory
from custom_components.doorman.yale.device import Device

from typing import List

from custom_components.doorman.yale.yale_api import YaleApi

from datetime import datetime

class YaleHub:
    def __init__(self, username, password, zone_id):
        self._LOGGER = logging.getLogger(__name__)
        self.yale_api = YaleApi(username, password)

        self.zone_id = zone_id

        self.state_data = UpdateWrapper(
            None,
            update_fn=self.get_state_data,
            access_fn=lambda x: x.data)
        self.state_history = UpdateWrapper(
            None,
            update_fn=self.get_state_history_data,
            access_fn=lambda x: x.data)

        self.devices = self.add_devices()

    def extract_message(self, json):
        self._LOGGER.debug("Extract message")
        status = json["message"]
        if status != "OK!":
            error_text = f"Status is not OK: {status}"
            self._LOGGER.error(error_text)
            raise YaleHubStatusException(error_text)
        return json.get("data")

    def get_state_data(self) -> ExpirationWrapper:
        self._LOGGER.debug("get_state_data")
        json = self.yale_api.get_state_data()
        message = self.extract_message(json)
        data = ExpirationWrapper(message, 10, None)
        return data

    def get_state_history_data(self) -> ExpirationWrapper:
        self._LOGGER.debug("get_state_history_data")
        json = self.yale_api.get_state_history_data()
        message = self.extract_message(json)
        data = ExpirationWrapper(message, 10, None)
        return data

    def add_devices(self) -> List[Device]:
        self._LOGGER.debug("add_devices")
        data = self.state_data.data

        new_devices = []
        devices = data.get("device_status")
        for device in devices:
            yale_device = DeviceFactory.Create(
                yale_hub=self,
                device_id=device.get("device_id"),
                device_type=device.get("type"),
                name=device.get("name"),
                area=device.get("area"),
                zone=device.get("no"))

            self._LOGGER.info(f"Adding device {yale_device.name}")
            new_devices.append(yale_device)
        return new_devices


