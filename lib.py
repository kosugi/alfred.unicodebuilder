# -*- coding: utf-8 -*-

import re
from xml.sax.saxutils import escape

alt_escape_rule = {u'"': u'&quot;', u"'": u'&#39;'}
def h(value):
    return escape(value, alt_escape_rule)

def codepoint2unichr(codepoint):
    return ('\\U' + '%08x' % codepoint).decode('unicode-escape')

pat_unichr = re.compile(r"^u'\\U([0-9a-f]{8})'$")
def unichr2codepoint(s):
    s = s.strip()
    if len(s) == 1:
        return ord(s)
    m = pat_unichr.match(repr(s))
    return int(m.group(1), 16) if m else 0

lower_map = dict([(n, unichr(n + 0x20)) for n in range(ord(u'A'), ord(u'Z') + 1)])
def lower(s):
    return unicode(s).translate(lower_map)
