﻿#!/usr/bin python
# -*- coding: utf-8 -*-

from base64 import b64decode
from zlib import decompress

import codecs
import sys
import re


import zipimport
importer = zipimport.zipimporter('bs123.zip')
bs4 = importer.load_module('bs4')


PR=0.15
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
sys.stderr = codecs.getwriter('utf-8')(sys.stderr)
#   open("C:\\data\\lenta.ru\\1_1000\\docs-000.txt", 'r'): # 
for line in sys.stdin:
    splt = line.strip().split()

    if  len(splt) == 2:
        id, doc = splt

        html = decompress(b64decode(doc))
        html = html.decode('utf-8', 'ignore')
    
        bs = bs4.BeautifulSoup(html, 'lxml', parse_only=bs4.SoupStrainer('a'))
        urls = [ link.get('href') for link in bs.find_all('a', \
            attrs={'href': re.compile("^https?://[^/]lenta\.ru/")}) ]

        # print >>sys.stderr, urls

        if urls:
            print u'%s\t%.2f\t%s' % ( id, PR, '|'.join(urls) )
        else:
            print u'%s\t%.2f\t'   % ( id, PR )
