#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys


# mapper
# читаем из стандартного входа
for line in sys.stdin: # для каждой поступающей строки
    if line.startswith('"'): continue

    # удаляем пробелы в начале и конце строки
    line = line.strip()

    # '6009554    pr=0.15    [4029274, ... ,5364047]'
    # разбиваем строчку на слова
    vertex, strPR, incident_verteces = line.split('\t')

    # посылаем структуру графа
    print '%s\tG\t%s' % (vertex, incident_verteces)
    
    PR = strPR.split('=')[1:]
    if PR: PR = float(PR[0])
    else: raise ValueError

    # получаем список инцидентности для вершины
    incident_verteces = incident_verteces.strip('[').rstrip(']')
    if len(incident_verteces):
        incident_verteces = list( incident_verteces.split(',') )
        # число инцидентных рёбер для данной вершины
        n_edges = len(incident_verteces)
    else: n_edges = 0

    for vertex in incident_verteces:
        # посылаем новое значение веса
        if n_edges: new_PR = (PR / n_edges)
        # патенты, которые ни на что не ссылаются
        else: new_PR = 0.

        print '%s\tW\t%f' % (vertex, new_PR)

"""
    есть патенты, которые ни на что не ссылаются
    есть патенты, на которые  ничто не ссылается

    В  первой ситуации вы должны правильно отработать отсутствие графа исходящих ссылок,
    Во второй поставить значение PR = (1-d) — минимальное или стартовое значение, о чем я говорил ранее.
    Для упрощения возьмем фиксированное количество итераций - 30.
"""
