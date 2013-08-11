# -*- coding: utf-8 -*-
from lxml import etree
from os.path import dirname, realpath
import sys
import codecs

BASE = realpath(dirname(sys.argv[0]))

with open(BASE + '/main.py') as f:
    src = f.read()
xml = etree.parse(BASE + '/info.plist.xml')
node = xml.xpath("/plist/dict/key[text()='objects']/following-sibling::array[1]/dict/key[text()='type']/following-sibling::string[1][text()='alfred.workflow.input.scriptfilter']/../key[text()='config']/following-sibling::dict[1]/key[text()='script']/following-sibling::string[1]")[0]
node.text = src
with codecs.getwriter('UTF-8')(open(BASE + '/info.plist', 'w')) as f:
    f.write(etree.tostring(xml))
