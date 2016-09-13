import os
import random
import unittest
from approvaltests import Approvals
from approvaltests.GenericDiffReporterFactory import GenericDiffReporterFactory
from Infrastructure.MobberManager import MobberManager


class TestsMobberManager(unittest.TestCase):
    def setUp(self):
        self.reporter = GenericDiffReporterFactory().get_first_working()

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
        mobber_manager.add_mobber("John")
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
        result = {"result": "Mobbers in List for Each Change\n", "increment": 0}

        def time_change_callback(mobber_list, driver_index, navigator_index):
            result["increment"] += 1
            result["result"] += "Action " + result["increment"].__str__() + ":"
            for mobber_index in range(0, mobber_list.__len__()):
                result["result"] += mobber_list[mobber_index]
                if mobber_index == driver_index:
                    result["result"] += " (Driver)"
                if mobber_index == navigator_index:
                    result["result"] += " (Navigator)"
                result["result"] += ", "

            result["result"] += "\n"

        mobber_manager.subscribe_to_mobber_list_change(time_change_callback)

        mobber_manager.add_mobber("Joe")
        mobber_manager.add_mobber("Chris")
        mobber_manager.add_mobber("Sam")
        mobber_manager.add_mobber("John")
        mobber_manager.switch_next_driver()
        mobber_manager.add_mobber("Bill")
        mobber_manager.switch_next_driver()
        mobber_manager.switch_next_driver()
        mobber_manager.switch_next_driver()
        mobber_manager.switch_next_driver()
        mobber_manager.switch_next_driver()
        mobber_manager.remove_mobber(2)
        mobber_manager.remove_mobber(0)
        mobber_manager.switch_next_driver()
        mobber_manager.rewind_driver()
        mobber_manager.add_mobber("Seth")
        mobber_manager.rewind_driver()
        mobber_manager.rewind_driver()
        mobber_manager.rewind_driver()
        mobber_manager.move_mobber_down(0)
        mobber_manager.add_mobber("Fredrick")
        mobber_manager.move_mobber_up(2)
        mobber_manager.remove_mobber(1)
        mobber_manager.remove_mobber(0)
        mobber_manager.remove_mobber(0)

        Approvals.verify(result["result"], self.reporter)

    def test_subscribe_to_mobber_list_changes_random(self):
        random.seed(0)
        mobber_manager = MobberManager(True)
        result = {"result": "Mobbers in List for Each Change\n", "increment": 0}

        def time_change_callback(mobber_list, driver_index, navigator_index):
            result["increment"] += 1
            result["result"] += "Action " + result["increment"].__str__() + ":"
            for mobber_index in range(0, mobber_list.__len__()):
                result["result"] += mobber_list[mobber_index]
                if mobber_index == driver_index:
                    result["result"] += " (Driver)"
                if mobber_index == navigator_index:
                    result["result"] += " (Next)"
                result["result"] += ", "

            result["result"] += "\n"

        mobber_manager.subscribe_to_mobber_list_change(time_change_callback)

        mobber_manager.add_mobber("Joe")
        mobber_manager.add_mobber("Chris")
        mobber_manager.add_mobber("Sam")
        mobber_manager.add_mobber("John")
        mobber_manager.switch_next_driver()
        mobber_manager.add_mobber("Bill")
        mobber_manager.switch_next_driver()
        mobber_manager.switch_next_driver()
        mobber_manager.switch_next_driver()
        mobber_manager.set_mobber_list(["Hello", "Eric", "Joe"])
        mobber_manager.switch_next_driver()
        mobber_manager.switch_next_driver()
        mobber_manager.remove_mobber(2)
        mobber_manager.remove_mobber(0)
        mobber_manager.switch_next_driver()
        mobber_manager.add_mobber("Seth")
        mobber_manager.move_mobber_down(0)
        mobber_manager.add_mobber("Fredrick")
        mobber_manager.move_mobber_up(2)
        mobber_manager.remove_mobber(1)
        mobber_manager.remove_mobber(0)
        mobber_manager.remove_mobber(0)

        Approvals.verify(result["result"], self.reporter)

    def test_navigator1_driver0_index(self):
        mobber_manager = MobberManager()
        mobber_manager.add_mobber("Joe")
        mobber_manager.add_mobber("Chris")
        result = "Navigator: " + str(mobber_manager.next_driver_index) + " Driver: " + str(mobber_manager.driver_index)
        self.assertEqual(result, "Navigator: 1 Driver: 0")

    def test_switch_navigator0_driver1_index(self):
        mobber_manager = MobberManager()
        mobber_manager.add_mobber("Joe")
        mobber_manager.add_mobber("Chris")
        mobber_manager.switch_next_driver()
        result = "Navigator: " + str(mobber_manager.next_driver_index) + " Driver: " + str(mobber_manager.driver_index)
        self.assertEqual(result, "Navigator: 0 Driver: 1")


if __name__ == '__main__':
    unittest.main()
