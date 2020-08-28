import unittest
from ddt import ddt, unpack, data

from custom_components.doorman.yale.expireable import Expireable
from datetime import datetime
import time

@ddt
class ExpirationDataTestMethod(unittest.TestCase):

    def test_generating_time_stamp(self):
        e_data = Expireable("test", None, 1)
        assert(e_data.timestamp != None)

    @data(("test", None, 1, 0, True),
          ("test", None, -1, 0, False),
          ("test", None, 100, 50, True),
          ("test", None, 50, 100, False))
    @unpack
    def test_is_active_true(self, _data, timestamp, validity_time, buffer, expected_result):

        e_data = Expireable(_data, validity_time, timestamp, buffer=buffer)

        self.assertEqual(e_data.is_active, expected_result)


if __name__ == '__main__':
    unittest.main()
