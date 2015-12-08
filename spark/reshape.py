#!/usr/bin python
# -*- coding: utf-8 -*-
import codecs
import sys
import re


# Используем unicode в стандартных потоках io
sys.stdin  = codecs.getreader('utf-8')(sys.stdin)
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
sys.stderr = codecs.getwriter('utf-8')(sys.stderr)
# type numerate | python reshape.py graph_pr graph_hits
with open(sys.argv[1], 'w') as f_pr_graph:
    with open(sys.argv[2], 'w') as f_hits_graph:
        for line in sys.stdin:
            line = line.rstrip(u'\n')

            count = line.count(u'\t')
            if   count == 2:
                print >>f_pr_graph, line
            elif count == 4:
                print >>f_hits_graph, line

