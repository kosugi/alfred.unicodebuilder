# -*- coding: utf-8 -*-

from os.path import dirname, realpath
import sys
import sqlite3
import unicodedata
from lib import codepoint2unichr

BASE = realpath(dirname(sys.argv[0]))

def prepare(conn):
    try:
        conn.execute('''drop table a''')
    except sqlite3.OperationalError:
        pass

    conn.execute('''create virtual table a using fts3 (code int primary key, name text)''')

def store(conn):
    for code in xrange(0x110000):
        if not code % 0x4000:
            print '{0:06X}'.format(code)
            conn.commit()
        c = codepoint2unichr(code)
        try:
            name = unicodedata.name(c)
        except ValueError:
            pass
        else:
            conn.execute('''insert into a (code, name) values (?, ?)''', (code, name))

with sqlite3.connect(BASE + '/db', isolation_level='EXCLUSIVE') as conn:
    prepare(conn)
    store(conn)
    conn.commit()
    conn.execute('''vacuum''')
