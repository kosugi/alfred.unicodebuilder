# -*- coding: utf-8 -*-

import re
import sqlite3
from contextlib import closing
from lib import lower, h, to_xml_item

pat_divide_kwds = re.compile(r'\s+')

def normalize_keywords(query):
    query = lower(query)
    for x in ('*', "'", '"', ':', '(', ')'):
        query = query.replace(x, ' ')

    kwds = []
    for kwd in pat_divide_kwds.split(query):
        if kwd:
            kwds.append(kwd + '*')
    return u' '.join(kwds)

def get_rows(cursor, query):
    cursor.execute('select code, name from a where kwd match ?', [normalize_keywords(query)])
    return cursor.fetchmany(30)

def error(s):
    return u'''<?xml version="1.0" encoding="UTF-8"?>
<items>
    <item uid="id" arg="{0}" valid="yes"><title>Error</title><subtitle>Something went wrong...</subtitle><icon>icon.png</icon></item>
</items>'''.format(h(s))

def build_xml(query, rows):
    items = []
    for row in rows:
        code = row[0]
        name = row[1]
        c = (r'\U' + '%08x' % code).decode('unicode-escape')
        params = {
            u'id': 'r' + str(code),
            u'arg': c,
            u'title': c,
            u'subtitle': u'U+%04X: %s' % (code, name),
            u'icon': u'icon.png',
            u'valid': u'yes'
        }
        items.append(to_xml_item(params))
    if not rows:
        params = {
            u'id': 'r0',
            u'arg': query,
            u'title': query,
            u'subtitle': u'No characters matched',
            u'icon': u'icon.png',
            u'valid': u'yes'
        }
        items.append(to_xml_item(params))

    return u'''<?xml version="1.0" encoding="UTF-8"?>
<items>{0}</items>'''.format(''.join(items))

def do(query):
    with sqlite3.connect('db') as conn:
        with closing(conn.cursor()) as cursor:
            try:
                rows = get_rows(cursor, query)
                return build_xml(query, rows)
            except Exception, e:
                return error(str(e))
