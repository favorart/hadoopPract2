#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import io

# reducer

res = {}
for line in sys.stdin: # для каждой посткпающейе строки
    # удаляем пробелы в начале и конце строки
    line = line.strip()

    # разбиваем строчку на слова
    v, mark, weight = line.split('\t')
    if v not in res:
        res[v] = [0,0]

    if ( mark == '1' ):
        res[v][0] += float(weight)
    elif ( mark == '0' ):
        res[v][1] = weight            
    
for k,v in res.items():
    print '%s\t%s\t%s' % (k, v[0], v[1])