# -*- coding: utf-8 -*-

import unicodedata
from lib import codepoint2unichr, h, to_xml_item

def parse_codepoint(query):
    return int(query, 16)

def to_xml(validity, query, title, subtitle):
    params = {
        u'id': 'id',
        u'arg': query,
        u'title': title,
        u'subtitle': subtitle,
        u'icon': u'icon.png',
        u'valid': [u'no', u'yes'][validity]
    }
    return u'''<?xml version="1.0" encoding="UTF-8"?>
<items>{0}</items>'''.format(to_xml_item(params))

def do(query):
    try:
        codepoint = parse_codepoint(query)
        s = codepoint2unichr(codepoint)
    except:
        return to_xml(False, query, query, u'Type hexadecimal unicode codepoint')

    try:
        name = unicodedata.name(s)
    except:
        return to_xml(False, query, query, u'Bad or unsuitable codepoint')
    else:
        return to_xml(True, s, u'{0}: {1}'.format(query, s), u'U+{0:04X}: {1}'.format(codepoint, name))
