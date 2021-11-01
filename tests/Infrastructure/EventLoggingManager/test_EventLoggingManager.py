import unittest
from unittest.mock import MagicMock

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


if __name__ == '__main__':
    unittest.main()
