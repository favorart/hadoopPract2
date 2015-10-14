#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
import operator
from collections import defaultdict
from itertools import groupby

# reducer

def key(d): return d.split('\t')[0]
for key, group in groupby([line.strip() for line in sys.stdin], key):    
    dic = defaultdict(int)
    for g in group:
        fields = re.split('\t|:', g)        
        field_i1, field_i2 = fields[1], fields[2]
        dic[field_i2] += 1

    sorted_dic = sorted(dic.items(), key=operator.itemgetter(1))

    n = len(dic)
    count_unique = n                                               #  1  Количество уникальных
    min  = sorted_dic[ 0][1]                                       #  2  Минимальное значение
    mid  = sorted_dic[int(n/2)][1]                                 #  3  Медиана
    max  = sorted_dic[-1][1]                                       #  4  Максимальное значение
    mean = (sum(   float(v)  for v in dic.values() ) / n)          #  5  Среднее значение
    devi = (sum( (v-mean)**2 for v in dic.values() ) / n) ** 0.5   #  6  Стандартное откланение

    print '%s\t%s\t%s\t%s\t%s\t%s\t%s' % (field_i1, count_unique, min, mid, max, mean, devi)


