import logging

import voluptuous as vol

from datetime import timedelta

import homeassistant.helpers.config_validation as cv
from homeassistant.components.lock import LockEntity, PLATFORM_SCHEMA
from homeassistant.const import CONF_ID, CONF_USERNAME, CONF_PASSWORD

DOMAIN = "doorman"
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_USERNAME): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
        vol.Required(CONF_ID): cv.string,
    }
)

SCAN_INTERVAL = timedelta(seconds=10)

_LOGGER = logging.getLogger(__name__)
_LOGGER.info("Initiating doorman module")

async def async_setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Doorman platform."""
    username = config.get(CONF_USERNAME)
    password = config.get(CONF_PASSWORD)


    login_data = login(username, password, initial_token)
    token = login_data["access_token"]
    device_id = config.get(CONF_ID)
    response = requests.get(API_STATE_URL, headers={"Authorization": f"Bearer {token}"}, timeout=5)
    if response.status_code == 200:
        _LOGGER.info("Setting up Doorman platform")
        data = response.json()
        status = data["message"]
        if status == "OK!":
            devices = data.get("data").get("device_status")
            for device in devices:
                device_id = device.get("device_id")
                name = device.get("name")
                state = device.get("status_open")[0]
                _LOGGER.info(f"Adding device {name}, setting status to {state}")
                add_entities(
                    [Doorman(state, login_data, username, password, name, device_id, initial_token)]
                )
        else:
            _LOGGER.info(f"Status is not OK!: {status}")
    else:
        _LOGGER.error("Error retrieving doorman lock status during init: %s", response.text)


# https://github.com/home-assistant/core/blob/master/homeassistant/components/lock/__init__.py#L114

class Doorman(LockEntity):
    """Representation of a Yale Doorman lock."""

    LOCK_STATE = "device_status.lock"
    UNLOCK_STATE = "device_status.unlock"
    FAILED_STATE = "failed"

    def __init__(self, name):
        """Initialize the lock."""
        self._state = state
        self._name = name

    @property
    def name(self):
        """Return the name of the device."""
        return self._name

    @property
    def is_locked(self):
        """Return True if the lock is currently locked, else False."""
        return self._state == Doorman.LOCK_STATE

    def lock(self, **kwargs):
        """Lock the device."""
        pass

    def unlock(self, **kwargs):
        """Unlock the device."""
        pass

    def update(self):
        """Update the internal state of the device."""
        states = self.get_state_history()
        for state in states:
            self._state = state
            self.async_write_ha_state()
        self._state = self.get_state()