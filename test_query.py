# -*- coding: utf-8 -*-

import unittest
from lib import call_with_cursor
from query import *

def squeeze(value):
    value = value.replace('\r', '')
    value = value.replace('\n', '')
    return value

class QueryTestCase(unittest.TestCase):

    def test_normalize_keywords(self):
        self.assertEqual(u'', normalize_keywords(u''))
        self.assertEqual(u'', normalize_keywords(u'*'))
        self.assertEqual(u'', normalize_keywords(u"'"))
        self.assertEqual(u'', normalize_keywords(u'"'))
        self.assertEqual(u'', normalize_keywords(u':'))
        self.assertEqual(u'', normalize_keywords(u'('))
        self.assertEqual(u'', normalize_keywords(u')'))
        self.assertEqual(u'a*', normalize_keywords(u'a'))
        self.assertEqual(u'a* b*', normalize_keywords(u' a B'))
        self.assertEqual(u'a* b*', normalize_keywords(u' A b'))
        self.assertEqual(u'Σ*', normalize_keywords(u'Σ'))
        self.assertEqual(u'б*', normalize_keywords(u'б'))

    def test_get_row_by_char(self):
        self.assertEqual((0xe5, 'LATIN SMALL LETTER A WITH RING ABOVE'), call_with_cursor(u'å', get_row_by_char))

    def test_error(self):
        self.maxDiff = None
        self.assertEqual(squeeze(error('bad')), u'''<?xml version="1.0" encoding="UTF-8"?><items><item uid="uid" arg="bad" valid="yes"><title>Error</title><subtitle>Something went wrong...</subtitle><icon>icon.png</icon></item></items>''')

    def test_do(self):
        self.maxDiff = None
        self.assertEqual(squeeze(do(u'')), u'''<?xml version="1.0" encoding="UTF-8"?><items><item uid="r0" arg="" valid="no"><title></title><subtitle>No characters matched</subtitle><icon>icon.png</icon></item></items>''')
        self.assertEqual(squeeze(do(u'å')), u'''<?xml version="1.0" encoding="UTF-8"?><items><item uid="r229" arg="\u00e5" valid="yes"><title>\u00e5</title><subtitle>U+00E5: LATIN SMALL LETTER A WITH RING ABOVE</subtitle><icon>icon.png</icon></item></items>''')
        self.assertEqual(squeeze(do(u'_dummy_')), u'''<?xml version="1.0" encoding="UTF-8"?><items><item uid="r0" arg="_dummy_" valid="no"><title>_dummy_</title><subtitle>No characters matched</subtitle><icon>icon.png</icon></item></items>''')
        self.assertEqual(squeeze(do(u'†')), u'''<?xml version="1.0" encoding="UTF-8"?><items><item uid="r8224" arg="\u2020" valid="yes"><title>\u2020</title><subtitle>U+2020: DAGGER</subtitle><icon>icon.png</icon></item></items>''')
        self.assertEqual(squeeze(do(u'fermata')), squeeze(u'''
<?xml version="1.0" encoding="UTF-8"?>
<items>
<item uid="r850" arg="\u0352" valid="yes"><title>\u0352</title><subtitle>U+0352: COMBINING FERMATA</subtitle><icon>icon.png</icon></item>
<item uid="r119056" arg="\ud834\udd10" valid="yes"><title>\ud834\udd10</title><subtitle>U+1D110: MUSICAL SYMBOL FERMATA</subtitle><icon>icon.png</icon></item>
<item uid="r119057" arg="\ud834\udd11" valid="yes"><title>\ud834\udd11</title><subtitle>U+1D111: MUSICAL SYMBOL FERMATA BELOW</subtitle><icon>icon.png</icon></item>
</items>
'''))

if __name__ == '__main__':
    unittest.main()
