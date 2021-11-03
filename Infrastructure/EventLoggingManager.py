from Infrastructure.FileUtilities import FileUtilities


class EventLoggingManager:

    def __init__(self, file_utility):
        self.file_utility = file_utility
        self.file_path = self.file_utility.go_up_dirs(self.file_utility.get_root_path(), 1) + "\\MobTimerEvents.log"

        if not self.file_utility.file_exists(self.file_path):
            self.file_utility.create_file(self.file_path)

    def log(self, data):
        self.file_utility.append(self.file_path, '\n' + data)
