#!/usr/bin python
# -*- coding: utf-8 -*-

import codecs
import sys
import re


# Используем unicode в стандартных потоках io
sys.stdin  = codecs.getreader('utf-8')(sys.stdin)
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
sys.stderr = codecs.getwriter('utf-8')(sys.stderr)


prev_id = None
ws = ""
us = ""

# type reduced | python reshape.py graph_pr graph_hits
with open(sys.argv[1], 'w') as f_pr_graph:
    with open(sys.argv[2], 'w') as f_hits_graph:

        # codecs.open("pagerank_spark/reduced1", 'r'): # 
        for line in sys.stdin:
            splt = line.strip().rstrip('\n').split('\t')

            if   len(splt) == 3:
                ws = splt[2]
                print >>f_pr_graph, '\t'.join(splt)
            
            elif len(splt) == 2:
                us = splt[1]
 
            if  prev_id and prev_id != splt[0]:
                print >>f_hits_graph, '%s\t%d\t%d\t%s\t%s' % ( prev_id, 1, 1, ws, us )
                ws, us = "", ""

            prev_id = splt[0]

