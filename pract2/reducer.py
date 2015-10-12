#!/usr/bin/env python
# -*- coding: utf-8 -*-

# reducer

from operator import itemgetter
import numpy as np
import sys
import os
import io


# для каждой посткпающей строки
# читаем из стандартного входа
for line in sys.stdin: 
    # удаляем пробелы в начале и конце строки
    line = line.strip()
    # разбиваем строчку на слова
    doc_id, doc = line.split()
    incident_docs[doc_id].append(doc)
   
print '%s\t0.15\t[%s]' % (doc_id, ','.join(incident_docs))