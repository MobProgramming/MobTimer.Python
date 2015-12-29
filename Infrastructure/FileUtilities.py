import imp
import os
import sys


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