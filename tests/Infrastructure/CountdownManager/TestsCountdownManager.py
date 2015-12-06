import datetime
import time
import unittest

from approvaltests import Approvals
from approvaltests.TextDiffReporter import TextDiffReporter

from Infrastructure.CountdownManager import CountdownManager


class TestsCountdownManager(unittest.TestCase):

    def test_set_countdown_timer(self):
        countdown_manager = CountdownManager(None)
        countdown_manager.set_countdown_duration(5, 14)
        result = "{}:{}".format(countdown_manager.minutes, countdown_manager.seconds)
        self.assertEqual("5:14", result)

    def test_new_countdown_timer(self):
        countdown_manager = CountdownManager(None)
        result = "{}:{}".format(countdown_manager.minutes, countdown_manager.seconds)
        self.assertEqual("0:0", result)

    def test_subscribe_to_time_changes(self):
        countdown_manager = CountdownManager(None)
        result = {"result": "Times changed to\n", "increment": 0}

        def time_change_callback(days, minutes, seconds):
            result["increment"] += 1
            result["result"] += "Action " + result["increment"].__str__() + ":"
            result["result"] += "    {0:0>2}:{1:0>2}".format(minutes, seconds) + "\n"

        countdown_manager.subscribe_to_time_changes(time_change_callback)
        countdown_manager.set_countdown_duration(4, 42)
        countdown_manager.set_countdown_duration(603, 52)
        countdown_manager.set_countdown_duration(1, 3)
        countdown_manager.set_countdown_duration(853, 32)
        countdown_manager.set_countdown_duration(3, 62)

        Approvals.verify(result["result"], TextDiffReporter())


if __name__ == '__main__':
    unittest.main()
