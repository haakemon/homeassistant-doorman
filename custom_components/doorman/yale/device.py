import logging
# from custom_components.doorman.yale.yale_hub import YaleHub

class Device():
    def __init__(self, yale_hub, device_id, name, area, zone):
        """Initialize device"""
        self._LOGGER = logging.getLogger(__name__)
        self.yale_hub = yale_hub
        self.device_id = device_id
        self.area = area
        self.zone = zone
        self._name = name

    @property
    def name(self):
        """Return the name of the device."""
        return self._name
