import os
import unittest

from approvaltests import Approvals
from approvaltests.TextDiffReporter import TextDiffReporter

from Infrastructure.MobberManager import MobberManager


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

    def test_clear(self):
        mobber_manager = MobberManager()
        mobber_manager.add_mobber("Joe")
        mobber_manager.add_mobber("Chris")
        mobber_manager.add_mobber("Sam")
        mobber_manager.clear()
        result = []
        self.assertEqual(mobber_manager.get_mobbers(), result)


    def test_subscribe_to_mobber_list_changes(self):
        mobber_manager = MobberManager()
        result = { "result" : "Mobbers in List for Each Change\n", "increment" : 0}

        def time_change_callback(mobber_list):
            result["increment"] += 1
            result["result"] += "Action " + result["increment"].__str__()  + ":"
            for mobber in mobber_list:
                result["result"] += mobber + ","
            result["result"] += "\n"

        mobber_manager.subscribe_to_mobber_list_change(time_change_callback)

        mobber_manager.add_mobber("Joe")
        mobber_manager.add_mobber("Chris")
        mobber_manager.add_mobber("Sam")
        mobber_manager.remove_mobber(2)
        mobber_manager.remove_mobber(0)
        mobber_manager.add_mobber("Seth")
        mobber_manager.move_mobber_down(0)
        mobber_manager.add_mobber("Fredrick")
        mobber_manager.move_mobber_up(2)
        mobber_manager.remove_mobber(1)
        mobber_manager.remove_mobber(0)
        mobber_manager.remove_mobber(0)

        Approvals.verify(result["result"], TextDiffReporter())

if __name__ == '__main__':
    os.environ["APPROVALS_TEXT_DIFF_TOOL"] = "meld"
    unittest.main()
