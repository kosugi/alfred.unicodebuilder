# -*- coding: utf-8 -*-

import unittest
from query import *

class QueryTestCase(unittest.TestCase):

    def test_normalize_keywords(self):
        self.assertEqual('', normalize_keywords(''))
        self.assertEqual('', normalize_keywords('*'))
        self.assertEqual('', normalize_keywords("'"))
        self.assertEqual('', normalize_keywords('"'))
        self.assertEqual('', normalize_keywords(':'))
        self.assertEqual('', normalize_keywords('('))
        self.assertEqual('', normalize_keywords(')'))
        self.assertEqual('a*', normalize_keywords('a'))
        self.assertEqual('a* b*', normalize_keywords(' a B'))
        self.assertEqual('a* b*', normalize_keywords(' a B'))
        self.assertEqual(u'Σ*', normalize_keywords(u'Σ'))
        self.assertEqual(u'б*', normalize_keywords(u'б'))

if __name__ == '__main__':
    unittest.main()
