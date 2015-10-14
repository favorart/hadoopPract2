#!/usr/bin/env python
# -*- coding: utf-8 -*-

from operator import itemgetter
import numpy as np
import sys
import os
import io

# type test.txt | python mapper_p1.py | sort | python reducer_p1.py | python mapper_p1.py | sort | python reducer_p1.py | sort > text.txt

# mapper

# читаем из стандартного входа
for line in sys.stdin: # для каждой поступающей строки
    # удаляем пробелы в начале и конце строки
    line = line.strip()
    # разбиваем строчку на слова
    vertex, weight, incident_verteces = line.split()
    # посылаем структуру графа
    print '%s\tG\t%s' % (vertex, incident_verteces)

    # получаем список инцидентности для вершины
    incident_verteces = incident_verteces.split(',')
    # число инцидентных рёбер
    n_edges = len(incident_verteces)
    
    for vertex in incident_verteces:
        # посылаем новое значение веса
        print '%s\tW\t%f' % (vertex, float(weight) / n_edges)

