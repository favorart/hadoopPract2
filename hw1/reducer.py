#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import operator
from collections import defaultdict

# reducer
dic = defaultdict(int)
for line in sys.stdin:
    field_i1, field_i2 = line.split('\t')
    dic[field_i2] += 1

sorted_dic = sorted(dic.items(), key=operator.itemgetter(1))

n = len(dic)
count_unique = n                       #  1  Количество уникальных
min  = sorted_dic[ 0][1]               #  2  Минимальное значение
mid  = sorted_dic[int(n/2)]            #  3  Медиана
max  = sorted_dic[-1][1]               #  4  Максимальное значение
mean = (sum( dic.values() ) / n)       #  5  Среднее значение
devi = (sum( (v - mean) ** 2 for v in dic.values() ) / n) ** 0.5 #  6  Стандартное откланение

print('\n uniques = %s\n min = %s\n median = %s\n max = %s\n mean = %s\n deviation = %s\n' % (count_unique, min, mid, max, mean, devi))

# min = float('+Inf')
# max = float('-Inf')

