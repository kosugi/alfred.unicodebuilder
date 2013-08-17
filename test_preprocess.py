# -*- coding: utf-8 -*-

import unittest
from preprocess import *

def squeeze(value):
    value = value.replace('\r', '')
    value = value.replace('\n', '')
    return value

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

    def test_do(self):
        self.maxDiff = None
        self.assertEqual(squeeze(do(u'')), u'''<?xml version="1.0" encoding="UTF-8"?><items><item uid="uid" arg="" valid="no"><title></title><subtitle>Type hexadecimal unicode codepoint</subtitle><icon>icon.png</icon></item></items>''')
        self.assertEqual(squeeze(do(u'a')), u'''<?xml version="1.0" encoding="UTF-8"?><items><item uid="uid" arg="a" valid="no"><title>a</title><subtitle>Bad or unsuitable codepoint</subtitle><icon>icon.png</icon></item></items>''')
        self.assertEqual(squeeze(do(u'0021')), u'''<?xml version="1.0" encoding="UTF-8"?><items><item uid="uid" arg="!" valid="yes"><title>0021: !</title><subtitle>U+0021: EXCLAMATION MARK</subtitle><icon>icon.png</icon></item></items>''')
        self.assertEqual(squeeze(do(u'200B')), u'''<?xml version="1.0" encoding="UTF-8"?><items><item uid="uid" arg="\u200b" valid="yes"><title>200B: \u200b</title><subtitle>U+200B: ZERO WIDTH SPACE</subtitle><icon>icon.png</icon></item></items>''')

if __name__ == '__main__':
    unittest.main()
