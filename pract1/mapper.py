#!/usr/bin/env python
# -*- coding: utf-8 -*-

from operator import itemgetter
import numpy as np
import sys
import os
import io

# type test.txt | python mapper.py | sort | python reducer.py | python mapper.py | sort | python reducer.py | sort > text.txt

# mapper

# читаем из стандартного входа
for line in sys.stdin: # для каждой посткпающейе строки
    # удаляем пробелы в начале и конце строки
    line = line.strip()
    # разбиваем строчку на слова
    words = line.split()
    print '%s\t%s\t%s' % (words[0], '0', words[2])

    where = words[2].split(',')
    N = len(where)
    for w in where:
        print '%s\t%s\t%s' % (w, '1', str(float(words[1]) / N))
