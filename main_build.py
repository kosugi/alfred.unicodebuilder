# -*- coding: utf-8 -*-
#
# makes a unicode character from keyword as hexadecimal codepoint
# and put it into clipboard.
#
# query MUST be escaped double quotation marks and backslashes.
#

import sys
import codecs
import build
sys.stdout = codecs.getwriter('UTF-8')(sys.stdout)
q = sys.argv[1].decode('UTF-8') if 1 < len(sys.argv) else u"""{query}"""
print build.do(q)
