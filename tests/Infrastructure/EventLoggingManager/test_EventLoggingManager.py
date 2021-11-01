import unittest
from unittest.mock import MagicMock

from Infrastructure.EventLoggingManager import EventLoggingManager
from Infrastructure.FileUtilities import FileUtilities


# 1. Mock remaining File Utilities function calls
# 2. Choose a real name for the log file

class TestsEventLoggingManager(unittest.TestCase):

    def test_log_file_should_be_created_if_doesnt_exist(self):
        # Options: Mocks, Fake Files

        # Arrange: Make sure the file does not exist
        file_utility = FileUtilities()
        file_utility.get_root_path = MagicMock(return_value='beginning of file path')
        file_utility.file_exists = MagicMock(return_value=False)
        file_utility.create_file = MagicMock(return_value=True)
        # Act: Instantiate EventLoggingManager
        event_logging_manager = EventLoggingManager(file_utility)

        # Assert: Verify the file exists
        file_utility.create_file.assert_called_with(file_utility.get_root_path() + "\\filename.txt")


if __name__ == '__main__':
    unittest.main()
