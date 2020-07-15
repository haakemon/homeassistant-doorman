import logging

from custom_components.doorman.yale.door import Door

class DeviceFactory:
    def __init__(self, yale_hub, device_id, device_type, name):
        if device_type == "device_type.door_lock":
            return Door(yale_hub, device_id, name, None)