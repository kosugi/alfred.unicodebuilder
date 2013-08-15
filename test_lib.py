# -*- coding: utf-8 -*-

import unittest
from lib import *

class LibTestCase(unittest.TestCase):

    def test_codepoint2unichr(self):
        self.assertEqual(u'\u0000', codepoint2unichr(0))
        self.assertEqual(u'\u00a0', codepoint2unichr(0xa0))
        self.assertEqual(u'\U00012000', codepoint2unichr(0x12000))

    def test_unichr2codepoint(self):
        try:
            self.assertEqual(0, unichr2codepoint(None))
            self.fail()
        except:
            self.assertTrue(True)
        self.assertEqual(0, unichr2codepoint(u''))
        self.assertEqual(0, unichr2codepoint(u' '))
        self.assertEqual(0, unichr2codepoint(u'  '))
        self.assertEqual(0x3042, unichr2codepoint(u'あ'))
        self.assertEqual(0x3042, unichr2codepoint(u' あ '))
        self.assertEqual(0x11d00, unichr2codepoint(u'\U00011d00'))

    def test_lower(self):
        self.assertEqual(u'', lower(u''))
        self.assertEqual(u'`', lower(u'`')) # a - 1
        self.assertEqual(u'a', lower(u'a'))
        self.assertEqual(u'z', lower(u'z'))
        self.assertEqual(u'{', lower(u'{')) # z + 1
        self.assertEqual(u'@', lower(u'@')) # A - 1
        self.assertEqual(u'a', lower(u'A'))
        self.assertEqual(u'z', lower(u'Z'))
        self.assertEqual(u'[', lower(u'[')) # Z + 1

if __name__ == '__main__':
    unittest.main()
