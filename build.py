# -*- coding: utf-8 -*-

from lib import codepoint2unichr, parse_codepoint, to_xml_item, to_xml, call_with_cursor

def make_xml(validity, arg, title, subtitle):
    return to_xml(dict(uid=to_xml_item(uid=u'uid', validity=validity, arg=arg, title=title, subtitle=subtitle)))

def get_name_by_code(cursor, code):
    cursor.execute('select name from a where code = ?', [code])
    return cursor.fetchone()[0]

def do(query):
    try:
        codepoint = parse_codepoint(query)
        s = codepoint2unichr(codepoint)
    except:
        return make_xml(False, query, query, u'Type hexadecimal unicode codepoint')

    try:
        name = call_with_cursor([codepoint], get_name_by_code)
    except:
        return make_xml(False, query, query, u'Bad or unsuitable codepoint')
    else:
        return make_xml(True, s, u'{0}: {1}'.format(query, s), u'U+{0:04X}: {1}'.format(codepoint, name))
