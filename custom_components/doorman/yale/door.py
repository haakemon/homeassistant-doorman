import logging

from custom_components.doorman.yale.device import Device

class Door(Device):
    """Representation of a Yale Doorman lock."""

    STATE_ENUM = {
        "1816": "device_status.lock",  # Locked after a failed lock
        "1815": "device_status.unlock",  # Failed to lock
        "1807": "device_status.lock",  # Auto-relocked
        "1801": "device_status.unlock",  # Unlock from inside
        "1802": "device_status.unlock",  # Unlock from outside, token or keypad,
    }

    NON_LOCK_EVENT = {"1602": "device_status.lock"}  # Periodic test

    LOCK_STATE = "device_status.lock"
    UNLOCK_STATE = "device_status.unlock"
    FAILED_STATE = "failed"

    def __init__(self, yale_hub, device_id, name, area, zone):
        """Initialize the lock."""

        super().__init__(
            yale_hub=yale_hub,
            device_id=device_id,
            name=name,
            area=area,
            zone=zone)

        self._LOGGER = logging.getLogger(__name__)
        self.report_ids = []

    @property
    def state(self):
        data = self.yale_hub.state_data.data
        devices = data.get("device_status")
        for device in devices:
            if self.device_id == device.get("device_id"):
                state = device.get("status_open")[0]
                return state

    @property
    def is_locked(self):
        """Return True if the lock is currently locked, else False."""
        return self.state == Door.LOCK_STATE

    def lock(self):
        """Lock the device."""
        self.yale_hub.yale_api.lock(self.area, self.zone)

    def unlock(self, pincode):
        """Unlock the device."""
        self.yale_hub.yale_api.unlock(self.area, self.zone, pincode)
