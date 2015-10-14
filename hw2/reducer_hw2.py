#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import defaultdict
import sys
import os
import io

# reducer

class graph_vertex(object):
    def __init__(self):
        self.id = None
        self.verteces = None
        self.weight = 0.

PR = 0.
dic = defaultdict(graph_vertex)
for line in sys.stdin: # для каждой посткпающейе строки
    # удаляем пробелы в начале и конце строки
    line = line.strip()

    # разбиваем строчку на слова
    vertex, mark, other = line.split('\t')

    if mark == 'W':
        dic[vertex].weight += float(other)
    else:
        if not PR:
            PR = PR.split('=')[1:]
            if PR: PR = float(PR[0])
            else: raise ValueError

        dic[vertex].verteces = other
        dic[vertex].vertex = vertex
    
for struct in dic.values():
    # отдаём очередную итерацию
    # + патенты, на которые никто не ссылается
    print '%s\t%f\t%s' % (struct.vertex, PR + (1. - PR) * struct.weight, struct.verteces)


