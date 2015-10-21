#!/usr/bin/env python
# -*- coding: utf-8 -*-

from itertools import groupby
from operator import itemgetter
import sys


# reducer
class graph_vertex(object):
    def __init__(self, vertex):
        self.vertex = vertex
        self.struct = None
        self.weight = 0.


defPR = 0.15
# для каждой посткпающей строки
for vertex, group in groupby((line.strip().split('\t', 1) for line in sys.stdin), itemgetter(0)):
    
    gv = graph_vertex(vertex)
    for v,g in group:
        # разбиваем строчку на слова
        mark, data = g.split('\t')

        if   mark == 'W': gv.weight += float(data)
        elif mark == 'G': gv.struct  = data
        else: raise ValueError

    # отдаём очередную итерацию
    # + патенты, на которые никто не ссылается
    print '%s\tpr=%f\t%s' % (gv.vertex, defPR + (1. - defPR) * gv.weight, gv.struct)

