#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import defaultdict
import sys
import os
import io

# reducer

class graph_vertex(object):
    def __init__(self):
        self.vertex = None
        self.verteces = None
        self.weight = 0.


defPR = 0.15
dic = defaultdict(graph_vertex)

for line in sys.stdin: # для каждой посткпающейе строки
    # удаляем пробелы в начале и конце строки
    line = line.strip()

    # разбиваем строчку на слова
    vertex, mark, other = line.split('\t')

    if   mark == 'W':
        dic[vertex].weight += float(other)
    elif mark == 'G':
        dic[vertex].verteces = other
        dic[vertex].vertex = vertex
    else: raise ValueError
    
for struct in dic.values():
    # отдаём очередную итерацию
    # + патенты, на которые никто не ссылается
    print '%s\tpr=%f\t%s' % (struct.vertex, defPR + (1. - defPR) * struct.weight, struct.verteces)

