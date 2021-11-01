import unittest
from unittest.mock import MagicMock
from approvaltests.approvals import verify

from Infrastructure.FileUtilities import FileUtilities
from Infrastructure.SettingsManager import SettingsManager


class EventLoggingManager:

    def __init__(self, file_utility):
        file_path = FileUtilities.get_root_path() + "\\filename.txt"
        if not file_utility.file_exists(file_path):
            # file_utility.
            file_utility.create_file(file_path)


class TestsEventLoggingManager(unittest.TestCase):

    def test_log_file_should_be_created_if_doesnt_exist(self):
        # Options: Mocks, Fake Files

        # Arrange: Make sure the file does not exist
        file_utility = FileUtilities()
        file_utility.file_exists = MagicMock(return_value=False)
        file_utility.create_file = MagicMock(return_value=True)
        # Act: Instantiate EventLoggingManager
        event_logging_manager = EventLoggingManager(file_utility)

        # Assert: Verify the file exists
        file_utility.create_file.assert_called_with(FileUtilities.get_root_path() + "\\filename.txt")


if __name__ == '__main__':
    unittest.main()
