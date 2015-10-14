#!/usr/bin/env python
# -*- coding: utf-8 -*-

from operator import itemgetter
import numpy as np
import sys
import os
import io

# mapper

PR = 0.
# читаем из стандартного входа
for line in sys.stdin: # для каждой поступающей строки
    if line.startswith('"'): continue

    # удаляем пробелы в начале и конце строки
    line = line.strip()

    # разбиваем строчку на слова
    # '6009554    pr=0.15    [4029274, ... ,5364047]'
    vertex, PR, incident_verteces = line.split('\t')

    # посылаем структуру графа
    print '%s\t%s\t%s' % (vertex, PR, incident_verteces)
    
    if not PR:
        PR = PR.split('=')[1:]
        if PR: PR = float(PR[0])
        else: raise ValueError

    # получаем список инцидентности для вершины
    incident_verteces = list(incident_verteces)
    # число инцидентных рёбер для данной вершины
    n_edges = len(incident_verteces)

    for vertex in incident_verteces:
        # посылаем новое значение веса
        if n_edges: new_PR = PR / n_edges
        else: new_PR = 0. # патенты, которые ни на что не ссылаются

        print '%s\tW\t%f' % (vertex, new_PR)

"""
    у вас есть патенты, которые ни на что не ссылаются
    у вас будут патенты, на которые никто не ссылается

    В  первой ситуации вы должны правильно отработать отсутствие графа исходящих ссылок,
    Во второй поставить значение PR = (1-d) — минимальное или стартовое значение, о чем я говорил ранее.
    Для упрощения возьмем фиксированное количество итераций - 30.
"""
