import unittest
from unittest.mock import call, MagicMock

from Infrastructure.EventLoggingManager import EventLoggingManager
from Infrastructure.FileUtilities import FileUtilities


class TestsEventLoggingManager(unittest.TestCase):

    def test_log_file_should_be_created_if_doesnt_exist(self):
        file_utility = FileUtilities()
        file_utility.get_root_path = MagicMock(return_value='beginning of file path')
        file_utility.file_exists = MagicMock(return_value=False)
        file_utility.create_file = MagicMock(return_value=True)

        EventLoggingManager(file_utility)

        file_utility.create_file.assert_called_with(file_utility.get_root_path() + '\\MobTimerEvents.log')

    def test_log_file_should_not_create_if_file_exists(self):
        file_utility = FileUtilities()
        file_utility.get_root_path = MagicMock(return_value='beginning of file path')
        file_utility.file_exists = MagicMock(return_value=True)
        file_utility.create_file = MagicMock(return_value=True)

        EventLoggingManager(file_utility)

        file_utility.create_file.assert_not_called()

    def test_log_file_should_append_to_log(self):
        file_utility = FileUtilities()
        file_utility.get_root_path = MagicMock(return_value='beginning of file path')
        file_utility.file_exists = MagicMock(return_value=True)
        file_utility.create_file = MagicMock(return_value=True)
        file_utility.append = MagicMock()
        logger = EventLoggingManager(file_utility)

        test_data = ["Hello world 1", "Hello world 2"]

        for entry in test_data:
            logger.log(entry)
        calls = []

        for entry in test_data:
            calls.append(call('beginning of file path\\MobTimerEvents.log', '\n'+entry))

        file_utility.append.assert_has_calls(calls)


if __name__ == '__main__':
    unittest.main()
