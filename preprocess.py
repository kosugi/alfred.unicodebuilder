# -*- coding: utf-8 -*-

import unicodedata
from lib import codepoint2unichr, h, to_xml_item, to_xml

def parse_codepoint(query):
    return int(query, 16)

def make_xml(validity, arg, title, subtitle):
    return to_xml(dict(uid=to_xml_item(uid=u'uid', validity=validity, arg=arg, title=title, subtitle=subtitle)))

def do(query):
    try:
        codepoint = parse_codepoint(query)
        s = codepoint2unichr(codepoint)
    except:
        return make_xml(False, query, query, u'Type hexadecimal unicode codepoint')

    try:
        name = unicodedata.name(s)
    except:
        return make_xml(False, query, query, u'Bad or unsuitable codepoint')
    else:
        return make_xml(True, s, u'{0}: {1}'.format(query, s), u'U+{0:04X}: {1}'.format(codepoint, name))
