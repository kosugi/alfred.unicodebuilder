# -*- coding: utf-8 -*-

import re
import sqlite3
from contextlib import closing
from xml.sax.saxutils import escape as h

pat_divide_kwds = re.compile(r'\s+')

def normalize_keywords(query):
    query = query.lower()
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

def to_xml_item(params):
    return u'''<item uid="{id}" arg="{arg}" valid="{valid}"><title>{title}</title><subtitle>{subtitle}</subtitle><icon>icon.png</icon></item>'''.format(**params)

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
            u'id': h('r' + str(code)),
            u'arg': h(c),
            u'title': h(c),
            u'subtitle': h(u'U+%04X: %s' % (code, name)),
            u'valid': u'yes'
        }
        items.append(to_xml_item(params))
    if not rows:
        params = {
            u'id': h('r0'),
            u'arg': h(query),
            u'title': h(query),
            u'subtitle': h(u'No characters matched'),
            u'valid': u'no'
        }
        items.append(to_xml_item(params))

    return u'''<?xml version="1.0" encoding="UTF-8"?>
<items>{0}</items>'''.format(''.join(items))

def do(query):
    with sqlite3.connect('db') as conn:
        with closing(conn.cursor()) as cursor:
            try:
                rows = get_rows(cursor, query)
                print build_xml(query, rows)
            except Exception, e:
                print error(str(e))