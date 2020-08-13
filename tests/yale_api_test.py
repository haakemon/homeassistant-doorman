import unittest

import logging
logging.basicConfig(filename='tests/yale_api.log', filemode='w', level=logging.DEBUG)

from custom_components.doorman.yale.yale_api import YaleApi
from custom_components.doorman.yale.exceptions import HttpResponseException, LoginException, UpdateException
from secrets import password, username, zone_id

from datetime import datetime
import time
import json


class YaleApiTestMethods(unittest.TestCase):

    _LOGGER = logging.getLogger(__name__)

    def test_login_access_token_present(self):
        self._LOGGER.info("Test: test_login_access_token_present")
        api = YaleApi(username, password)

        json_response = api.login()
        actual_result = "access_token" in json_response

        self.assertTrue(actual_result)

    def test_login_error_present(self):
        self._LOGGER.info("Test: test_login_error_present")

        self.assertRaises(LoginException, YaleApi, "username", "password")

    def test_get_access_token_correct_cred(self):
        self._LOGGER.info("Test: test_get_access_token_correct_cred")
        api = YaleApi(username, password)

        token = api.token.data

        self.assertIsNotNone(token)

    def test_get_access_token_incorrect_cred(self):
        self._LOGGER.info("Test: test_get_access_token_incorrect_cred")
        api = YaleApi(username, password)

        # force an update of token witch will fail due to wrong password
        api.password = "wrong"
        api.token._data = None

        with self.assertRaises(UpdateException) as context:
            i = api.token.data

    def test_get_states_data(self):
        self._LOGGER.info("Test: test_get_states_data")
        api = YaleApi(username, password)

        data = api.get_state_data()

        with open('tests/yale_api_states.txt', 'w') as outfile:
            json.dump(data, outfile)
        self.assertTrue(True)

    def test_get_state_history_data(self):
        self._LOGGER.info("Test: test_get_state_history_data")
        api = YaleApi(username, password)

        data = api.get_state_history_data()

        with open('tests/yale_api_states_history.txt', 'w') as outfile:
            json.dump(data, outfile)
        self.assertTrue(True)

    def test_unlock(self):
        self._LOGGER.info("Test: Unlock doors")
        api = YaleApi(username, password)

        data = api.unlock(1, 2, "xxxxxx")

        with open('tests/yale_api_lock_doors.txt', 'a+') as outfile:
            json.dump(data, outfile)
        self.assertTrue(True)

    def test_lock(self):
        self._LOGGER.info("Test: Unlock doors")
        api = YaleApi(username, password)

        # data = api.lock(1, 1)  # Carport
        data = api.lock(1, 2)  # Main
        # data = api.lock(1, 3)  # Back

        with open('tests/yale_api_unlock_doors.txt', 'a+') as outfile:
            json.dump(data, outfile)
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
