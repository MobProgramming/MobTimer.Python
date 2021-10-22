import unittest

import sys

import os
from Infrastructure.TipsManager import TipsManager


class TestsTipsManage(unittest.TestCase):
    def test_random_tip_from_file(self):
        seed = 0

        dirname = os.path.dirname(__file__)
        path = self.go_two_dirs_up(dirname) + "\\Tips"
        tips_manager = TipsManager(seed, path)
        result = tips_manager.get_random_tip()
        self.assertEqual(result, 'TestTips2.txt: Words\n')

    def go_two_dirs_up(self, dirname):
        return "\\".join(dirname.split('\\')[:-2])

    def test_random_tip_from_file_second(self):
        seed = 1
        dirname = os.path.dirname(__file__)
        path = self.go_two_dirs_up(dirname) + "\\Tips"
        tips_manager = TipsManager(seed, path)
        result = tips_manager.get_random_tip()
        self.assertEqual(result, 'TestTips.txt: Customer collaboration over contract negotiation\n')


if __name__ == '__main__':
    unittest.main()
