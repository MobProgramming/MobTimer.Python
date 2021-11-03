import unittest

import sys

import os

from Infrastructure.FileUtilities import FileUtilities
from Infrastructure.TipsManager import TipsManager


class TestsTipsManage(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.fileUtilities = FileUtilities()

    def test_random_tip_from_file(self):
        seed = 0

        dirname = os.path.dirname(__file__)
        path = self.fileUtilities.go_up_dirs(dirname, 2) + "\\Tips"
        tips_manager = TipsManager(seed, path)
        result = tips_manager.get_random_tip()
        self.assertEqual(result, 'TestTips2.txt: Words\n')


    def test_random_tip_from_file_second(self):
        seed = 1
        dirname = os.path.dirname(__file__)
        path = self.fileUtilities.go_up_dirs(dirname, 2) + "\\Tips"
        tips_manager = TipsManager(seed, path)
        result = tips_manager.get_random_tip()
        self.assertEqual(result, 'TestTips.txt: Customer collaboration over contract negotiation\n')

    def test_random_tip_from_file_second_alternate_slashes(self):
        seed = 1
        dirname = os.path.dirname(__file__)
        path = self.fileUtilities.go_up_dirs(dirname, 2) + "\\Tips"
        path = path.replace("\\", "/")
        tips_manager = TipsManager(seed, path)
        result = tips_manager.get_random_tip()
        self.assertEqual(result, 'TestTips.txt: Customer collaboration over contract negotiation\n')


if __name__ == '__main__':
    unittest.main()
