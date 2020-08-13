import unittest
from ddt import data, ddt, unpack

import logging
logging.basicConfig(filename='tests/update_wrapper_test.log', filemode='w', level=logging.DEBUG)

from custom_components.doorman.yale.update_wrapper import UpdateWrapper
from custom_components.doorman.yale.exceptions import UpdateException


class stub_test:
    def __init__(self, i):
        self.i = i

@ddt
class TestUpdateWrapper(unittest.TestCase):

    _LOGGER = logging.getLogger(__name__)

    def test_wrapper_1_update_manual(self):
        self._LOGGER.info("Test: test_wrapper_1_no_update")
        initial_data = 1
        update_wrapper = UpdateWrapper(initial_data, update_fn=lambda: 5)
        self.assertEqual(update_wrapper.data, 1)

    def test_wrapper_1_update_auto(self):
        self._LOGGER.info("Test: test_wrapper_1_update_auto")
        initial_data = None
        update_wrapper = UpdateWrapper(initial_data, update_fn=lambda: 5)

        self.assertEqual(update_wrapper.data, 5)

    def test_wrapper_1_access_fn(self):
        self._LOGGER.info("Test: test_wrapper_1_access_fn_no_update")
        initial_data = stub_test(1)
        update_wrapper = UpdateWrapper(initial_data, update_fn=lambda: stub_test(5), access_fn=lambda x: x.i)

        self.assertEqual(update_wrapper.data, 1)

    def test_wrapper_1_access_fn_auto(self):
        self._LOGGER.info("Test: test_wrapper_1_access_fn_update")
        initial_data = stub_test(None)
        update_wrapper = UpdateWrapper(initial_data, update_fn=lambda: stub_test(5), access_fn=lambda x: x.i)

        self.assertEqual(update_wrapper.data, 5)

    def test_wrapper_1_update_fail_return_none(self):
        self._LOGGER.info("Test: test_wrapper_1_update_fail_return_none")
        initial_data = None
        update_wrapper = UpdateWrapper(initial_data, update_fn=lambda: None)

        with self.assertRaises(UpdateException) as context:
            i = update_wrapper.data

if __name__ == '__main__':
    unittest.main()
