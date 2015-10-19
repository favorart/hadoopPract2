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


dic = defaultdict(graph_vertex)
for line in sys.stdin: # для каждой посткпающейе строки
    # удаляем пробелы в начале и конце строки
    line = line.strip()

    # разбиваем строчку на слова
    vertex, mark, other = line.split('\t')

    # dic[vertex] = [weight, verteces]         
    if   mark == 'G':
        dic[vertex].verteces = other
        dic[vertex].vertex = vertex
    elif mark == 'W':
        dic[vertex].weight += float(other)
    else:
        raise ValueError
    
for struct in dic.values():
    # отдаём очередную итерацию
    print '%s\t%f\t%s' % (struct.vertex, struct.weight, struct.verteces)


