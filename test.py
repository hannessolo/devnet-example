import unittest
import main

class TestFindInterface(unittest.TestCase):

    def test_normal(self):
        interface2 = {"name": "GigabitEthernet2", "active": False}
        interfaces = [{"name": "GigabitEthernet0", "active": False}, {"name": "GigabitEthernet1", "active": True}, interface2]

        self.assertEqual(main.find_interface("GigabitEthernet2", interfaces), interface2)

    def test_empty(self):
        interfaces = []
        self.assertIsNone(main.find_interface("GigabitEthernet2", interfaces))

    def test_duplicate(self):
        interfaces = [{"name": "GigabitEthernet1", "active": False}, {"name": "GigabitEthernet1", "active": True}]
        self.assertEqual(main.find_interface("GigabitEthernet1", interfaces), {"name": "GigabitEthernet1", "active": False})


if __name__ == '__main__':
    unittest.main()