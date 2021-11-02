from Infrastructure.FileUtilities import FileUtilities


class EventLoggingManager:

    def __init__(self, file_utility):
        self.file_path = file_utility.get_root_path() + "\\MobTimerEvents.log"
        self.file_utility = file_utility
        if not self.file_utility.file_exists(self.file_path):
            self.file_utility.create_file(self.file_path)

    def log(self, data):
        self.file_utility.append(self.file_path, '\n' + data)
