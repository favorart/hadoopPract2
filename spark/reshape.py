#!/usr/bin python
# -*- coding: utf-8 -*-

import codecs
import sys
import re


# type numerated | python reshape.py  graph_pr graph_hits
fn_graph_pr   = sys.argv[1] if len(sys.argv) > 1 else 'graph_pr'
fn_graph_hits = sys.argv[2] if len(sys.argv) > 1 else 'graph_hits'

# Используем unicode в стандартных потоках io
sys.stdin  = codecs.getreader('utf-8')(sys.stdin)
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
sys.stderr = codecs.getwriter('utf-8')(sys.stderr)

# with open(fn_graph_pr, 'w') as f_pr_graph:
#     with open(fn_graph_hits, 'w') as f_hits_graph:
# 
#         for line in sys.stdin:
#             line = line.rstrip(u'\n')
# 
#             count = line.count(u'\t')
#             if   count == 2:
#                 print >>f_pr_graph, line
#             elif count == 4:
#                 print >>f_hits_graph, line
# 

# ==================================================
# ОШИБКА ПОСЛЕ ПЕРЕНУМЕРАЦИИ - была решена топором


numbers_pr = {}
numbers_ht = {}
# i = 0
for line in open('spark/numerated', 'r'): #sys.stdin:
    splt = line.rstrip(u'\n').split('\t')

    # if not (i % 1000): print '.',
    if  len(splt) == 3:
        if  splt[0] not in numbers_pr:
            v = set(splt[2].split(',')) if len(splt[2]) else set()
            numbers_pr[ splt[0] ] = v

        elif len(splt[2]):
            numbers_pr[ splt[0] ].update(splt[2].split(','))
                
    elif len(splt) == 5:
        if  splt[0] not in numbers_ht:
            ws = set(splt[3].split('|')) if len(splt[3]) else set()
            us = set(splt[4].split('|')) if len(splt[4]) else set()
            numbers_ht[ splt[0] ] = (ws, us)
    
        else:
            if len(splt[3]):
                numbers_ht[ splt[0] ][0].update(splt[3].split('|'))
            if len(splt[4]):
                numbers_ht[ splt[0] ][1].update(splt[4].split('|'))
    # i += 1


with open(fn_graph_pr, 'w') as f_pr_graph:
    for k,v in numbers_pr.items():
        v = sorted(v)
        print >>f_pr_graph, '%s\t0.15\t%s' % (k, ','.join(v))
            

with open(fn_graph_hits, 'w') as f_hits_graph:
    for k,v in numbers_ht.items():
        ws,us = v
        ws = sorted(ws)
        us = sorted(us)
        print >>f_hits_graph, '%s\t1\t1\t%s\t%s' % (k, ','.join(ws), ','.join(us))

