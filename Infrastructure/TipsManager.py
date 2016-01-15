import os, random

from Infrastructure.PathUtility import PathUtility


class TipsManager(object):
    def __init__(self, seed = None):
        if seed is not None:
            random.seed(seed)

    def get_random_tip(self):
        tips_folder = "Tips"
        random_file = random.choice(os.listdir("%s" % tips_folder))
        return "{}: {}" .format(random_file, TipsManager.random_line(PathUtility.normalize_path(tips_folder + "\\" + random_file)))

    @staticmethod
    def random_line(file_name):
        with open(file_name) as a_file:
            line = next(a_file)
            for num, aline in enumerate(a_file):
              if random.randrange(num + 2): continue
              line = aline
            return line