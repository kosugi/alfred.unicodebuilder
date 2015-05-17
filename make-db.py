# -*- coding: utf-8 -*-

from contextlib import closing
from os.path import dirname, realpath
from lib import parse_codepoint
import re
import sys
import sqlite3

BASE = realpath(dirname(sys.argv[0]))
re_line = re.compile('^([0-9A-F]+)\t(.*)$')

def prepare(conn):
    try:
        conn.execute('''drop table a''')
    except sqlite3.OperationalError:
        pass

    conn.execute('''create virtual table a using fts3 (code int primary key, name text)''')

def store(conn):
    with open(BASE + '/build/NamesList.txt') as f:
        for line in f.readlines():
            m = re_line.match(line)
            if not m:
                continue
            code, name = m.groups()
            if name in ('<control>', '<not a character>'):
                continue
            conn.execute('''insert into a (code, name) values (?, ?)''', (parse_codepoint(code), name))

if __name__ == '__main__':
    with sqlite3.connect(BASE + '/build/db', isolation_level='EXCLUSIVE') as conn:
        prepare(conn)
        store(conn)
        conn.commit()
        conn.execute('''vacuum''')
