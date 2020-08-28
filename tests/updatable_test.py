import unittest
from custom_components.doorman.yale.updateable import Updateable

class stub_test(Updateable):
    def __init__(self, valid_time):
        super().__init__("Initial", valid_time)
        self.i = 0

    def update(self):
        self.i += 1
        return self.i


# if debuging, observ that the property can be accessed when stoping

class TestUpdateWrapper(unittest.TestCase):

    def test_updateable_should_update_correct(self):
        test = stub_test(-1)
        data = test.data
        self.assertEqual(data, 1)

    def test_updateable_should_not_update_correct(self):
        test2 = stub_test(100000000000)
        data = test2.data
        self.assertEqual(data, "Initial")

if __name__ == '__main__':
    unittest.main()
