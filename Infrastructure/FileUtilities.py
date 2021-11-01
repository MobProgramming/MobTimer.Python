import imp
import os
import sys
from os.path import exists


class FileUtilities(object):
    @staticmethod
    def main_is_frozen():
       return (hasattr(sys, "frozen") or # new py2exe
               hasattr(sys, "importers") # old py2exe
               or imp.is_frozen("__main__")) # tools/freeze

    @staticmethod
    def get_root_path():
        if FileUtilities.main_is_frozen():
            return os.path.dirname(sys.executable)
        return os.path.dirname(os.path.realpath(__file__))

    def file_exists(self, path):
        return exists(path)

    def create_file(self, filePath):
        f = open(filePath, "w")
        # f.write("Woops! I have deleted the content!")
        f.close()

    # def __init__(self, file_utility):
    #
    #     if not file_utility.file_exists():
    #         file_utility.create_file("path to file")