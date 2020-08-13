import unittest

import logging
logging.basicConfig(filename='tests/yale_hub.log', filemode='w', level=logging.DEBUG)

from custom_components.doorman.yale.yale_hub import YaleHub
from custom_components.doorman.yale.door import Door
from custom_components.doorman.yale.exceptions import LoginException

from secrets import password, username, zone_id
from datetime import datetime
import time
import json
import copy

class YaleHubTestMethods(unittest.TestCase):
    _LOGGER = logging.getLogger(__name__)


class YaleHubTestData(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(YaleHubTestData, self).__init__(*args, **kwargs)
        self._LOGGER = logging.getLogger(__name__)
        self.yale_hub = YaleHub(username, password, zone_id)

    def test_get_states_data(self):
        self._LOGGER.info("Test: test_get_states_data")

        state_data = self.yale_hub.state_data.data

        with open('tests/yale_hub_states_data2.txt', 'w') as outfile:
            json.dump(state_data, outfile)
        self.assertTrue(True)

    def test_validate_devices(self):
        devices = self.yale_hub.devices

        names = [i.name for i in devices]

        self.assertEqual(['Carport', 'Main', 'Back'], names)

        devices[1].lock()

        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
