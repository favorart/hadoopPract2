#!/usr/bin python
# -*- coding: utf-8 -*-
import codecs
import sys
import re

# Используем unicode в стандартных потоках io
sys.stdin  = codecs.getreader('utf-8')(sys.stdin)
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
sys.stderr = codecs.getwriter('utf-8')(sys.stderr)

prev_url = ""
ws = []

# type numerate | python reducer.py | sort > reduced

# open("pagerank_spark/numerate", 'r'): #
for line in sys.stdin:
    splt = line.strip().rstrip('\n').split('\t')

    if  len(splt) == 2:
        url, id = splt
        del splt
        
        if  prev_url and prev_url != url:
            print u'%s\t%s' % (url, ','.join(ws) )
            ws = []

        ws.append(id)
        prev_url = url

    elif len(splt) == 3:
        print line

