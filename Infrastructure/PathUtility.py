import os
import sys


class PathUtility(object):
    @staticmethod
    def normalize_path(path, root=sys.argv[0]):
        path = path.replace('\\', '/')
        if not path.startswith("/"):
            path = "/" + path
        dirname = os.path.dirname(root)
        path = dirname + path
        path = path.replace('\\', '/')
        return path
