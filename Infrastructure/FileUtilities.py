import imp
import os
import sys
from os.path import exists


class FileUtilities(object):
    @staticmethod
    def main_is_frozen():
        return (hasattr(sys, "frozen") or  # new py2exe
                hasattr(sys, "importers")  # old py2exe
                or imp.is_frozen("__main__"))  # tools/freeze

    def get_root_path(self):
        if FileUtilities.main_is_frozen():
            return os.path.dirname(sys.executable)
        return os.path.dirname(os.path.realpath(__file__))

    def file_exists(self, file_path):
        return exists(file_path)

    def create_file(self, file_path):
        f = open(file_path, "w")
        f.close()

    def append(self, file_path, data):
        f = open(file_path, "a")
        f.write(data)
        f.close()

    def go_up_dirs(self, root_directory, levels):
        if '\\' in root_directory:
            return "/".join(root_directory.split('\\')[:-levels])
        else:
            return "/".join(root_directory.split('/')[:-levels])