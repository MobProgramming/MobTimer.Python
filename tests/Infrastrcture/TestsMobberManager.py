import unittest


class MobberManager(object):
    def __init__(self):
        self.mobber_list = []

    def mobber_count(self):
        return 0

    def add_mobber(self, mobber_name):
        self.mobber_list.append(mobber_name)

    def get_mobbers(self):
        return self.mobber_list


class TestsMobberManager(unittest.TestCase):
    def test_emty_mobber_manager_has_no_items(self):
        mobber_manager = MobberManager()
        self.assertEqual(mobber_manager.mobber_count(), 0)

    def test_add_mobber_chris_has_chris(self):
        mobber_manager = MobberManager()
        mobber_manager.add_mobber("Chris")
        result = ["Chris"]
        self.assertEqual(mobber_manager.get_mobbers(), result)


    def test_add_mobber_joe_chris_has_joe_chris(self):
        mobber_manager = MobberManager()
        mobber_manager.add_mobber("Joe")
        mobber_manager.add_mobber("Chris")
        result = ["Joe", "Chris"]
        self.assertEqual(mobber_manager.get_mobbers(), result)


if __name__ == '__main__':
    unittest.main()
