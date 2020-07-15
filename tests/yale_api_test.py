import unittest
from ddt import data, ddt, unpack
import logging
logging.basicConfig(filename='tests/example.log', filemode='w', level=logging.DEBUG)

from custom_components.doorman.yale.yale_api import YaleApi
from custom_components.doorman.yale.exceptions import LoginException
from secrets import password, username, zone_id

from datetime import datetime
import time
import json

@ddt
class YaleApiTestMethods(unittest.TestCase):

    _LOGGER = logging.getLogger(__name__)

    @data((username, password, zone_id, True), ("username", "password", zone_id, False))
    @unpack
    def test_login_access_token_present(self, _username, _password, _zone_id, expected_result):
        YaleApiTestMethods._LOGGER.info("Test: test_login_access_token_present")
        json_response = YaleApi.login(_username, _password, _zone_id)

        actual_result = "access_token" in json_response

        self.assertEqual(actual_result, expected_result)

    @data((username, password, zone_id, False), ("username", "password", zone_id, True))
    @unpack
    def test_login_error_present(self, _username, _password, _zone_id, expected_result):
        YaleHubMethods._LOGGER.info("Test: test_login_error_present")
        yale_hub = YaleHub(_username, _password, _zone_id)

        login_data = yale_hub.login()

        actual_result = "error" in login_data

        self.assertEqual(actual_result, expected_result)

    def test_get_access_token_correct_cred(self):
        YaleHubMethods._LOGGER.info("Test: test_get_access_token_correct_cred")
        yale_hub = YaleHub(username, password, zone_id)

        token = yale_hub.get_access_token()

        self.assertIsNotNone(token)

    def test_get_access_token_incorrect_cred(self):
        YaleHubMethods._LOGGER.info("Test: test_get_access_token_incorrect_cred")
        yale_hub = YaleHub(username, "password", zone_id)

        self.assertRaises(LoginException, yale_hub.get_access_token)

    def test_get_states_data(self):
        YaleHubMethods._LOGGER.info("Test: test_get_states_data")
        yale_hub = YaleHub(username, password, zone_id)

        data = yale_hub.get_state_data()

        with open('tests/states_data.txt', 'w') as outfile:
            json.dump(data.data, outfile)
        self.assertTrue(True)

    def test_get_state_history_data(self):
        YaleHubMethods._LOGGER.info("Test: test_get_state_history_data")
        yale_hub = YaleHub(username, password, zone_id)

        data = yale_hub.get_state_history_data()

        with open('tests/states_history_data.txt', 'w') as outfile:
            json.dump(data.data, outfile)
        self.assertTrue(True)

class YaleHubTest_data(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(YaleHubTest_data, self).__init__(*args, **kwargs)
        self._LOGGER = logging.getLogger(__name__)
        self.yale_hub = YaleHub(username, password, zone_id)

    def test_get_states_data(self):
        self._LOGGER.info("Test: test_get_states_data")

        data = self.yale_hub.state_data

        with open('tests/states_data2.txt', 'w') as outfile:
            json.dump(data.data, outfile)
        self.assertTrue(True)

    def test_get_states_data_twice_data_not_expired(self):
        self._LOGGER.info("Test: test_get_states_data_twice_data_not_expired")



        data = self.yale_hub.state_data._data

        data2 = self.yale_hub.state_data._data

        self.assertEqual(data.timestamp, data2.timestamp)

    def test_get_states_data_twice_data_expired(self):
        self._LOGGER.info("Test: test_get_states_data_twice_data_expired")

        data = self.yale_hub.state_data.data

        self.yale_hub.state_data._data.time_valid = -1

        data2 = self.yale_hub.state_data.data

        self.assertNotEqual(data.timestamp, data2.timestamp)



if __name__ == '__main__':
    unittest.main()
