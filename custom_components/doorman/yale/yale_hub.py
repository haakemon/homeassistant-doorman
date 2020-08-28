import logging
import requests
from custom_components.doorman.yale.updateable import Updateable

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

        self.state = State(self.yale_api)
        self.state_history = StateHistory(self.yale_api)

        self.devices = self.add_devices()

    def add_devices(self) -> List[Device]:
        self._LOGGER.debug("add_devices")
        data = self.state.data

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

    def get_state(self, device_id):
        data = self.state.data
        devices = data.get("device_status")
        state = [i for i in devices if i.get("device_id") == device_id]
        if len(state == 1):
            return state[0]
        raise Exception(f"State was not found for id: {device_id}")


class State(Updateable):
    def __init__(self, yale_api):
        super().__init__(None, 10)

        self.yale_api = yale_api

    def update(self):
        message = self.yale_api.get_state_data()
        return message

class StateHistory(Updateable):
    def __init__(self, yale_api):
        super().__init__(None, 10)

        self.yale_api = yale_api

    def update(self):
        message = self.yale_api.get_state_history_data()
        return message
