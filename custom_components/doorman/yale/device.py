import logging

class Device():
    def __init__(self, yale_hub, device_id, type, name):
        """Initialize device"""
        self._LOGGER = logging.getLogger(__name__)
        self.yale_hub = yale_hub
        self.device_id = device_id
        self.type = type
        self._name = name

    @property
    def name(self):
        """Return the name of the device."""
        return self._name
