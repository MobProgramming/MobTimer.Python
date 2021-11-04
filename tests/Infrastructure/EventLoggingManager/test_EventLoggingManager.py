import unittest
from unittest.mock import call, MagicMock, Mock

from Infrastructure.DateTimeUtility import DateTimeUtility
from Infrastructure.EventLoggingManager import EventLoggingManager
from Infrastructure.FileUtilities import FileUtilities


class TestsEventLoggingManager(unittest.TestCase):

    def test_log_file_should_be_created_if_doesnt_exist(self):
        file_utility = FileUtilities()
        beginning_of_file_path = 'beginning of file path'
        file_utility.get_root_path = MagicMock(return_value=beginning_of_file_path + "\\Infrastructure")
        file_utility.file_exists = MagicMock(return_value=False)
        file_utility.create_file = MagicMock(return_value=True)
        date_time_utility = DateTimeUtility()
        EventLoggingManager(file_utility,date_time_utility)

        file_utility.create_file.assert_called_with(beginning_of_file_path + '\\MobTimerEvents.log')

    def test_log_file_should_not_create_if_file_exists(self):
        file_utility = FileUtilities()
        file_utility.get_root_path = MagicMock(return_value='beginning of file path' + '\\Infrastructure')
        file_utility.file_exists = MagicMock(return_value=True)
        file_utility.create_file = MagicMock(return_value=True)

        date_time_utility = DateTimeUtility()
        EventLoggingManager(file_utility, date_time_utility)

        file_utility.create_file.assert_not_called()

    def test_log_file_should_append_to_log(self):
        file_utility = FileUtilities()
        beginning_of_file_path = 'beginning of file path'
        file_utility.get_root_path = MagicMock(return_value=beginning_of_file_path + '\\Infrastructure')
        file_utility.file_exists = MagicMock(return_value=True)
        file_utility.create_file = MagicMock(return_value=True)
        file_utility.append = MagicMock()
        date_time_utility = DateTimeUtility()

        timestamps = [1594823426.159446, 1594123426.159447, 1594654426.159448]
        date_time_utility.get_timestamp = Mock()
        date_time_utility.get_timestamp.side_effect = timestamps
        logger = EventLoggingManager(file_utility, date_time_utility)

        test_data = ["Hello world 1", "Hello world 2"]

        for entry in test_data:
            logger.log(entry)
        calls = []
        index = 0
        for entry in test_data:
            calls.append(call(f'{beginning_of_file_path}\\MobTimerEvents.log', f'\n{timestamps[index]} {entry}'))
            index += 1

        file_utility.append.assert_has_calls(calls)


if __name__ == '__main__':
    unittest.main()
