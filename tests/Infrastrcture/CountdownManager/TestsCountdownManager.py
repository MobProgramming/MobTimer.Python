import unittest

from approvaltests import Approvals
from approvaltests.TextDiffReporter import TextDiffReporter


class CountdownManager(object):
    def __init__(self, root_tk_app):
        self.minutes = 0
        self.seconds = 0
        self.time_change_callbacks = []

        self.root_tk_app = root_tk_app
        self.refresh_timer()

    def set_countdown_duration(self, minutes, seconds):
        self.minutes = minutes
        self.seconds = seconds
        self.fire_time_change_callbacks()

    def subscribe_to_time_changes(self, time_change_callback):
        self.time_change_callbacks.append(time_change_callback)

    def fire_time_change_callbacks(self):
        for callback in self.time_change_callbacks:
            if callback:
                callback(self.minutes, self.seconds)

    def refresh_timer(self):
        if self.root_tk_app:
            self.root_tk_app.after(1000, self.refresh_timer)


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

        def time_change_callback(minutes, seconds):
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
