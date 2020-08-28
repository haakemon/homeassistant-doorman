
import logging
_LOGGER = logging.getLogger(__name__)

import voluptuous as vol
from datetime import timedelta

import homeassistant.helpers.config_validation as cv
from homeassistant.components.lock import LockEntity, PLATFORM_SCHEMA
from homeassistant.const import CONF_USERNAME, CONF_PASSWORD

from custom_components.doorman.yale.yale_hub import YaleHub
from custom_components.doorman.yale.door import Door

DOMAIN = "doorman"
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_USERNAME): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
    }
)

SCAN_INTERVAL = timedelta(seconds=10)

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Doorman platform."""
    _LOGGER.info("Initiating doorman module")

    username = config[CONF_USERNAME]
    password = config.get(CONF_PASSWORD)

    yale_hub = YaleHub(username=username, password=password, zone_id=1)

    doormans = [Doorman(i) for i in yale_hub.devices]
    add_entities(doormans)


# https://github.com/home-assistant/core/blob/master/homeassistant/components/lock/__init__.py#L114
class Doorman(LockEntity):
    """Representation of a Yale Doorman lock."""

    def __init__(self, door: Door):
        self.yale_door = door

    @property
    def name(self):
        """Return the name of the device."""
        return self.yale_door.name

    @property
    def is_locked(self):
        """Return True if the lock is currently locked, else False."""
        return self.yale_door.is_locked

    def lock(self, **kwargs):
        """Lock the device."""
        self.yale_door.lock()

    def unlock(self, **kwargs):
        """Unlock the device."""
        _LOGGER.debug(f"Unlock kwargs: {kwargs}")
        self.yale_door.unlock(kwargs.get('code', ""))

    def update(self):
        self.yale_door.update_state()
