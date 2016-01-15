import os
import sys


class PathUtility(object):
    @staticmethod
    def normalize_path(path):

        if not path.startswith("/"):
            path = "/" + path
        # if sys.frozen == 'macosx_app':
        #     path = path + "/Resources/"
        path = path.replace('\\','/')
        result = os.path.dirname(sys.argv[0]) + path
        return result