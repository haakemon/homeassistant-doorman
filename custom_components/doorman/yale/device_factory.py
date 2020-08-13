import logging

from custom_components.doorman.yale.door import Door

class DeviceFactory:

    @staticmethod
    def Create(yale_hub, device_id, device_type, name, area, zone):
        if device_type == "device_type.door_lock":
            return Door(
                yale_hub=yale_hub,
                device_id=device_id,
                name=name,
                area=area,
                zone=zone)
