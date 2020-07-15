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

    def __init__(self, yale_hub, device_id, name, state):
        """Initialize the lock."""
        Device.__init__(yale_hub, device_id, name)

        self._LOGGER = logging.getLogger(__name__)
        self._state = state
        self.report_ids = []

    @property
    def is_locked(self):
        """Return True if the lock is currently locked, else False."""
        return self._state == Door.LOCK_STATE

    def lock(self, **kwargs):
        """Lock the device."""
        # self._state = self.do_change_request(Doorman.LOCK_STATE)

    def unlock(self, **kwargs):
        """Unlock the device."""
        # self._state = self.do_change_request(Doorman.UNLOCK_STATE)

    def get_state(self):
        data = self.get_state_data()

        devices = data.get("device_status")
        for device in devices:
            device_id = device.get("device_id")
            name = device.get("name")
            state = device.get("status_open")[0]
            if name == self._name:
                if state != Door.LOCK_STATE and state != Door.UNLOCK_STATE:
                    self._LOGGER.info(f"Setting state to {state}")
                return state

    def get_state_history(self):
        data = self.get_state_history_data()
        states = []

        for event in data:
            device_type = event.get("type")
            if device_type == "device_type.door_lock":
                report_id = event.get("report_id")
                if report_id not in self.report_ids:
                    name = event.get("name")
                    user = event.get("user")
                    event_type = event.get("event_type")
                    self.report_ids.append(report_id)
                    if event_type in self.NON_LOCK_EVENT:
                        continue
                    state = self.STATE_ENUM[event_type]
                    self._LOGGER.info(f"Parsing event: {report_id} it has {state}")
                    states.append(state)

        return states
