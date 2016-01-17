import unittest

import sys

from Infrastructure.TipsManager import TipsManager


class TestsTipsManage(unittest.TestCase):
    def test_random_tip_from_file(self):
        seed = 0
        tips_manager = TipsManager(seed,sys.argv[1])
        result = tips_manager.get_random_tip()
        self.assertEqual(result, 'TestTips2.txt: Words\n')

    def test_random_tip_from_file_second(self):
        seed = 1
        tips_manager = TipsManager(seed,sys.argv[1])
        result = tips_manager.get_random_tip()
        self.assertEqual(result, 'TestTips.txt: Customer collaboration over contract negotiation\n')


if __name__ == '__main__':
    unittest.main()
