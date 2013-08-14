# -*- coding: utf-8 -*-

from os.path import dirname, realpath
import sys
import sqlite3
import unicodedata

BASE = realpath(dirname(sys.argv[0]))

def prepare(conn):
    try:
        conn.execute('''drop table a''')
    except sqlite3.OperationalError:
        pass

    conn.execute('''create virtual table a using fts3 (code int primary key, name text, kwd text)''')

def store(conn):
    for code in xrange(0x110000):
        if not code % 0x4000:
            print '{0:06X}'.format(code)
            conn.commit()
        c = ('\\U' + '%08x' % code).decode('unicode-escape')
        try:
            name = unicodedata.name(c)
        except ValueError:
            pass
        else:
            kwd = name if code < 0x80 else name + ' '  + c
            conn.execute('''insert into a (code, name, kwd) values (?, ?, ?)''', (code, name, kwd))

with sqlite3.connect(BASE + '/db', isolation_level='EXCLUSIVE') as conn:
    prepare(conn)
    store(conn)
    conn.commit()
    conn.execute('''vacuum''')
