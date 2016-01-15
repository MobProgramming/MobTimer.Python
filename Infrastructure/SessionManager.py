import os

from Infrastructure.PathUtility import PathUtility
from Infrastructure.FileUtilities import FileUtilities


class SessionManager(object):
    def __init__(self, uuid_generator):
        self.uuid_generator = uuid_generator

    def create_session(self):
        session_id = self.uuid_generator.uuid1()

        directory = self.get_sessions_path()

        file = open(directory + session_id.__str__(), 'w+')

    def get_sessions_path(self):
        directory = (FileUtilities.get_root_path() + "/Sessions/")
        if not os.path.exists(directory):
            os.makedirs(directory)
        return directory

    def get_active_sessions(self):
        return os.listdir(self.get_sessions_path())

    def clear_sessions(self):
        folder = self.get_sessions_path()
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception:
                pass



