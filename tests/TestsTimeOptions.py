import unittest


class TimeOptionsManager(object):
    def __init__(self):
        self.minutes = 10
        self.seconds = 0

    def get_time_string(self):
        return "{0:0>2}:00".format(self.minutes, self.seconds)

    def indement_minutes(self):
        self.minutes += 1

    def decriment_minutes(self):
        self.minutes -= 1


class TestsTimeOptions(unittest.TestCase):
    def test_default_time_10_minutes(self):
        time_options_manager = TimeOptionsManager()
        result = time_options_manager.get_time_string()
        self.assertEqual(result, "10:00")

    def test_indement_minutes_once_is_11_minutes(self):
        time_options_manager = TimeOptionsManager()
        time_options_manager.indement_minutes()
        result = time_options_manager.get_time_string()
        self.assertEqual(result, "11:00")

    def test_decriment_minutes_once_is_9_minutes(self):
        time_options_manager = TimeOptionsManager()
        time_options_manager.decriment_minutes()
        result = time_options_manager.get_time_string()
        self.assertEqual(result, "09:00")


if __name__ == '__main__':
    unittest.main()
