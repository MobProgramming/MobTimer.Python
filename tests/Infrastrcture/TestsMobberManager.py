import unittest


class MobberManager(object):
    def __init__(self):
        self.mobber_list = []

    def mobber_count(self):
        return self.mobber_list.__len__()

    def add_mobber(self, mobber_name):
        self.mobber_list.append(mobber_name)

    def get_mobbers(self):
        return self.mobber_list

    def remove_mobber(self, remove_mobber_index):
        if self.mobber_count() == 0: return
        del self.mobber_list[remove_mobber_index]

    def move_mobber_up(self, swap_index):
        if self.mobber_count() == 0: return
        destination_index = swap_index - 1
        self.mobber_list[swap_index], self.mobber_list[destination_index] = self.mobber_list[destination_index], \
                                                                            self.mobber_list[swap_index]

    def move_mobber_down(self, swap_index):
        if self.mobber_count() == 0: return
        destination_index = (swap_index + 1) % self.mobber_list.__len__()
        self.mobber_list[swap_index], self.mobber_list[destination_index] = self.mobber_list[destination_index], \
                                                                            self.mobber_list[swap_index]


class TestsMobberManager(unittest.TestCase):
    def test_empty_mobber_manager_has_no_items(self):
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

    def test_add_mobber_joe_chris_joe__remove_joe_has_joe_chris(self):
        mobber_manager = MobberManager()
        mobber_manager.add_mobber("Joe")
        mobber_manager.add_mobber("Chris")
        mobber_manager.add_mobber("Joe")
        mobber_manager.remove_mobber(2)
        result = ["Joe", "Chris"]
        self.assertEqual(mobber_manager.get_mobbers(), result)

    def test_add_4_mobbers_move_up_middle(self):
        mobber_manager = MobberManager()
        mobber_manager.add_mobber("Joe")
        mobber_manager.add_mobber("Chris")
        mobber_manager.add_mobber("Will")
        mobber_manager.add_mobber("Eric")
        mobber_manager.move_mobber_up(2)
        result = ["Joe", "Will", "Chris", "Eric"]
        self.assertEqual(mobber_manager.get_mobbers(), result)

    def test_add_4_mobbers_move_up_top(self):
        mobber_manager = MobberManager()
        mobber_manager.add_mobber("Joe")
        mobber_manager.add_mobber("Chris")
        mobber_manager.add_mobber("Will")
        mobber_manager.add_mobber("Eric")
        mobber_manager.move_mobber_up(0)
        result = ["Eric", "Chris", "Will", "Joe"]
        self.assertEqual(mobber_manager.get_mobbers(), result)

    def test_add_4_mobbers_move_down_middle(self):
        mobber_manager = MobberManager()
        mobber_manager.add_mobber("Joe")
        mobber_manager.add_mobber("Chris")
        mobber_manager.add_mobber("Will")
        mobber_manager.add_mobber("Eric")
        mobber_manager.move_mobber_down(2)
        result = ["Joe", "Chris", "Eric", "Will"]
        self.assertEqual(mobber_manager.get_mobbers(), result)

    def test_add_4_mobbers_move_down_bottom(self):
        mobber_manager = MobberManager()
        mobber_manager.add_mobber("Joe")
        mobber_manager.add_mobber("Chris")
        mobber_manager.add_mobber("Will")
        mobber_manager.add_mobber("Eric")
        mobber_manager.move_mobber_down(3)
        result = ["Eric", "Chris", "Will", "Joe"]
        self.assertEqual(mobber_manager.get_mobbers(), result)

    def test_move_down_empty(self):
        mobber_manager = MobberManager()
        mobber_manager.move_mobber_down(0)
        result = []
        self.assertEqual(mobber_manager.get_mobbers(), result)

    def test_move_up_empty(self):
        mobber_manager = MobberManager()
        mobber_manager.move_mobber_up(0)
        result = []
        self.assertEqual(mobber_manager.get_mobbers(), result)

    def test_remove_empty(self):
        mobber_manager = MobberManager()
        mobber_manager.remove_mobber(0)
        result = []
        self.assertEqual(mobber_manager.get_mobbers(), result)

    def test_subscribe_to_mobber_list_changes(self):
        mobber_manager = MobberManager()
        result = { "result" : "Contents:"}

        def time_change_callback(mobber_list):
            result["result"] += " ["
            for mobber in mobber_list:
                result["result"] += mobber + ","
            result["result"] += "], "

        mobber_manager.subscribe_to_mobber_list_change(time_change_callback)

        mobber_manager.add_mobber("Joe")
        mobber_manager.add_mobber("Chris")
        mobber_manager.add_mobber("Sam")
        mobber_manager.remove_mobber(2)

        self.assertEqual(result["result"], "Contents:[], [Joe,], [Joe,Chris,], [Joe,Chris,Sam,], [Joe,Chris,]")


if __name__ == '__main__':
    unittest.main()
