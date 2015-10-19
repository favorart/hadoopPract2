#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import defaultdict
from itertools import groupby
from operator import itemgetter
import numpy as np
import sys
import os
import io

# reducer

dic = defaultdict(list)
for line in sys.stdin: 
    line = line.strip()
    doc_id, doc = line.split()
    dic[doc_id].append(doc)

for doc_id,docs in dic.items():
    print '%s\tpr=0.15\t[%s]' % ( doc_id, ','.join(docs) )


""" 
    Для расчета определим условия:
    Значение переменной d установим как 0.85, стартовое значение PR установим как (1-d) = 0.15

    В качестве исходных данных возьмем файл на кластере /data/patents/cite75_99.txt, который состоит из двух столбцов:
    CITING - патент, который ссылается; CITED - патент, на который ссылаются

    Нужно написать задачу, которая приводит исходные данные в нужный нам, описаный:
     <citing> \t <pr=(1-d)=0.15> \t <[CITED1[, CITED2[...[,CITEDn]]]]>
"""
