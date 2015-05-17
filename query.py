# -*- coding: utf-8 -*-

from lib import lower, h, to_xml_item, to_xml, unichr2codepoint, codepoint2unichr, normalize, call_with_cursor
import re

pat_divide_kwds = re.compile(r'\s+')
def normalize_keywords(query):
    query = normalize(query)
    query = lower(query)
    for x in ('*', "'", '"', ':', '(', ')'):
        query = query.replace(x, ' ')

    kwds = []
    for kwd in pat_divide_kwds.split(query):
        if kwd:
            kwds.append(kwd + '*')
    return u' '.join(kwds)

def row_into_items(items, row):
    code, name = row
    c = codepoint2unichr(code)
    items[code] = to_xml_item(
        uid='r' + str(code),
        arg=c,
        title=c,
        subtitle=u'U+%04X: %s' % (code, name))

def get_row_by_char(cursor, query):
    try:
        code = unichr2codepoint(query)
        cursor.execute('select code, name from a where code = ?', [code])
        return cursor.fetchone()
    except:
        pass

def get_rows(cursor, query):
    cursor.execute('select code, name from a where name match ?', [normalize_keywords(query)])
    return cursor.fetchmany(30)

def empty_result_into_items(items, query):
    items[0] = to_xml_item(
        uid='r0',
        arg=query,
        title=query,
        subtitle=u'No characters matched',
        validity=False)

def error(s):
    return to_xml(dict(uid=to_xml_item(uid=u'uid', arg=s, title=u'Error', subtitle=u'Something went wrong...')))

def make_results(cursor, query):
    items = {}
    try:
        row = get_row_by_char(cursor, query)
        if row:
            row_into_items(items, row)

        rows = get_rows(cursor, query)
        for row in rows:
            row_into_items(items, row)

        if not items:
            empty_result_into_items(items, query)

        return to_xml(items)
    except Exception, e:
        return error(str(e))

def do(query):
    return call_with_cursor([query], make_results)
