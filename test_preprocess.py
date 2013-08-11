# -*- coding: utf-8 -*-

import unittest
from preprocess import *

class PreprocessTestCase(unittest.TestCase):

    def test_parse_codepoint(self):
        try:
            self.assertEqual(0, parse_codepoint(''))
            self.fail()
        except:
            self.assertTrue(True)

        self.assertEqual(0, parse_codepoint('0'))
        self.assertEqual(0x10, parse_codepoint('10'))
        self.assertEqual(0x12000, parse_codepoint('012000'))

    def test_codepoint2unichr(self):
        self.assertEqual(u'\u0000', codepoint2unichr(0))
        self.assertEqual(u'\u00a0', codepoint2unichr(0xa0))
        self.assertEqual(u'\U00012000', codepoint2unichr(0x12000))






if __name__ == '__main__':
    unittest.main()
