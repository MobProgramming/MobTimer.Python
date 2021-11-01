from Infrastructure.FileUtilities import FileUtilities


class EventLoggingManager:

    def __init__(self, file_utility):
        file_path = file_utility.get_root_path() + "\\filename.txt"
        if not file_utility.file_exists(file_path):
            file_utility.create_file(file_path)