import unittest


class TimeOptionsManager(object):
    def __init__(self):
        self.minutes = 10
        self.seconds = 0
        self.time_change_callbacks = []

    def get_time_string(self):
        return "{0:0>2}:{1:0>2}".format(self.minutes, self.seconds)

    def increment_minutes(self):
        self.minutes += 1
        self.fire_time_change_callbacks()

    def decriment_minutes(self):
        self.minutes -= 1
        self.fire_time_change_callbacks()

    def increment_seconds(self):
        self.seconds = (self.seconds + 15) % 60
        self.fire_time_change_callbacks()

    def decrement_seconds(self):
        self.seconds = ((self.seconds + 60) - 15) % 60
        self.fire_time_change_callbacks()

    def subscribe_to_timechange(self, time_change_callback):
        self.time_change_callbacks.append(time_change_callback)

    def fire_time_change_callbacks(self):
        for time_change_callback in self.time_change_callbacks:
            if time_change_callback:
                time_change_callback(self.get_time_string())


class TestsTimeOptions(unittest.TestCase):
    def test_default_time_10_minutes(self):
        time_options_manager = TimeOptionsManager()
        result = time_options_manager.get_time_string()
        self.assertEqual(result, "10:00")

    def test_indement_minutes_once_is_11_minutes(self):
        time_options_manager = TimeOptionsManager()
        time_options_manager.increment_minutes()
        result = time_options_manager.get_time_string()
        self.assertEqual(result, "11:00")

    def test_decriment_minutes_once_is_9_minutes(self):
        time_options_manager = TimeOptionsManager()
        time_options_manager.decriment_minutes()
        result = time_options_manager.get_time_string()
        self.assertEqual(result, "09:00")

    def test_increment_seconds_once_is_10_minutes_15_seconds(self):
        time_options_manager = TimeOptionsManager()
        time_options_manager.increment_seconds()
        result = time_options_manager.get_time_string()
        self.assertEqual(result, "10:15")

    def test_increment_seconds_4_times_is_10_minutes(self):
        time_options_manager = TimeOptionsManager()
        time_options_manager.increment_seconds()
        time_options_manager.increment_seconds()
        time_options_manager.increment_seconds()
        time_options_manager.increment_seconds()
        result = time_options_manager.get_time_string()
        self.assertEqual(result, "10:00")

    def test_decrement_seconds_once_is_10_minutes_45_seconds(self):
        time_options_manager = TimeOptionsManager()
        time_options_manager.decrement_seconds()
        result = time_options_manager.get_time_string()
        self.assertEqual(result, "10:45")

    def test_decrement_seconds_3_times_is_10_minutes_45_seconds(self):
        time_options_manager = TimeOptionsManager()
        time_options_manager.decrement_seconds()
        time_options_manager.decrement_seconds()
        time_options_manager.decrement_seconds()
        result = time_options_manager.get_time_string()
        self.assertEqual(result, "10:15")

    def test_subscribe_to_time_changes(self):
        time_options_manager = TimeOptionsManager()
        result = { "result" : "time"}

        def time_change_callback(time):
            result["result"] += " " + time

        time_options_manager.subscribe_to_timechange(time_change_callback)

        time_options_manager.increment_seconds()

        self.assertEqual(result["result"], "time 10:15")


if __name__ == '__main__':
    unittest.main()
