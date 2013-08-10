# -*- coding: utf-8 -*-
#
# makes a unicode character from keyword as hexadecimal codepoint
# and put it into clipboard.
#
# query MUST be escaped double quotation marks and backslashes.
#

import sys
import codecs
import preprocess
sys.stdout = codecs.getwriter('UTF-8')(sys.stdout)
print preprocess.do(u"""{query}""")
