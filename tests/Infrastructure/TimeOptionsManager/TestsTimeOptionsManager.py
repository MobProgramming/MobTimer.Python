import os
import unittest

from approvaltests import Approvals
from approvaltests.TextDiffReporter import TextDiffReporter

from Infrastructure.TimeSettingsManager import TimeSettingsManager


class TestsTimeOptionsManager(unittest.TestCase):
    def test_default_time_10_minutes(self):
        time_options_manager = TimeSettingsManager()
        result = time_options_manager.get_time_string()
        self.assertEqual(result, "10:00")

    def test_increment_minutes_once_is_11_minutes(self):
        time_options_manager = TimeSettingsManager()
        time_options_manager.increment_minutes()
        result = time_options_manager.get_time_string()
        self.assertEqual(result, "11:00")

    def test_decrement_minutes_once_is_9_minutes(self):
        time_options_manager = TimeSettingsManager()
        time_options_manager.decrement_minutes()
        result = time_options_manager.get_time_string()
        self.assertEqual(result, "09:00")

    def test_increment_seconds_once_is_10_minutes_15_seconds(self):
        time_options_manager = TimeSettingsManager()
        time_options_manager.increment_seconds()
        result = time_options_manager.get_time_string()
        self.assertEqual(result, "10:15")

    def test_increment_seconds_4_times_is_10_minutes(self):
        time_options_manager = TimeSettingsManager()
        time_options_manager.increment_seconds()
        time_options_manager.increment_seconds(1)
        time_options_manager.increment_seconds()
        time_options_manager.increment_seconds()
        result = time_options_manager.get_time_string()
        self.assertEqual(result, "10:46")

    def test_decrement_seconds_once_is_10_minutes_45_seconds(self):
        time_options_manager = TimeSettingsManager()
        time_options_manager.decrement_seconds()
        result = time_options_manager.get_time_string()
        self.assertEqual(result, "10:45")

    def test_decrement_seconds_3_times_is_10_minutes_45_seconds(self):
        time_options_manager = TimeSettingsManager()
        time_options_manager.decrement_seconds()
        time_options_manager.decrement_seconds(1)
        time_options_manager.decrement_seconds()
        result = time_options_manager.get_time_string()
        self.assertEqual(result, "10:29")

    def test_subscribe_to_time_changes(self):
        time_options_manager = TimeSettingsManager()
        result = {"result": "time"}

        def time_change_callback(time, minutes, seconds,origin_station_name):
            result["result"] += " " + time

        time_options_manager.subscribe_to_timechange(time_change_callback)

        time_options_manager.increment_seconds()

        self.assertEqual(result["result"], "time 10:00 10:15")

    def test_subscribe_to_time_changes_complex(self):
        time_options_manager = TimeSettingsManager()
        result = {"result": "Time Options after Change:", "increment" : 0}

        def time_change_callback(time, minutes, seconds,origin_station_name):
            result["increment"] += 1
            result["result"] += "\n Change " + result["increment"].__str__() + "| " + time

        time_options_manager.subscribe_to_timechange(time_change_callback)

        time_options_manager.increment_seconds()
        time_options_manager.increment_seconds()
        time_options_manager.increment_seconds()
        time_options_manager.decrement_seconds()
        time_options_manager.decrement_seconds()
        time_options_manager.decrement_seconds()
        time_options_manager.decrement_seconds()
        time_options_manager.decrement_minutes()
        time_options_manager.decrement_minutes()
        time_options_manager.increment_minutes()
        time_options_manager.increment_minutes()
        time_options_manager.increment_minutes()
        time_options_manager.increment_minutes()
        time_options_manager.increment_minutes()
        time_options_manager.set_countdown_time(3, 14)

        Approvals.verify(result["result"], TextDiffReporter())

if __name__ == '__main__':
    os.environ["APPROVALS_TEXT_DIFF_TOOL"] = "meld"
    unittest.main()
