# -*- coding: utf-8 -*-
from lxml import etree
from os.path import dirname, realpath
import sys
import codecs

def xpath_for_uid(uid):
    return ''.join((
        "/plist",
        "/dict",
        "/key[text()='objects']",
        "/following-sibling::array[1]",
        "/dict",
        "/key[text()='uid']"
        "/following-sibling::string[1][text()='%s']",
        "/..",
        "/key[text()='config']",
        "/following-sibling::dict[1]",
        "/key[text()='script']",
        "/following-sibling::string[1]",
    )) % uid # !! not to be escaped !!

def replace_node(xml, uid, path):
    with open(path) as f:
        src = f.read()
    node = xml.xpath(xpath_for_uid(uid))[0]
    node.text = src

BASE = realpath(dirname(sys.argv[0]))
xml = etree.parse(BASE + '/info.plist.xml')
replace_node(xml, '6A8652AA-89BD-4559-B9E5-F27D3D01C0CA', BASE + '/main_build.py')
replace_node(xml, 'ADAA3DC1-80FE-4CBE-9698-6E5AE51B3791', BASE + '/main_query.py')

with codecs.getwriter('UTF-8')(open(BASE + '/info.plist', 'w')) as f:
    f.write(etree.tostring(xml))
