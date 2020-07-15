from custom_components.doorman.log.log_wrapper import logger
import logging
import unittest

logging.basicConfig(filename='tests/log_test.log', filemode='w', level=logging.DEBUG)

class TestLog(unittest.TestCase):

    @logger
    def test_logging(self):
        log = logging.getLogger(__name__)
        log.debug("Inside function")
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
