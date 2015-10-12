#!/usr/bin/env python
# -*- coding: utf-8 -*-

from operator import itemgetter
import numpy as np
import sys
import os
import io

# type test.txt | python mapper.py | sort | python reducer | python mapper.py | sort | python reducer.py

# mapper

# NO_DOC  0.15  NO_DOC,NO_DOC,NO_DOC,...

# для каждой посткпающей строки
# читаем из стандартного входа
for line in sys.stdin: 
    # line = line.strip()
    line = re.sub(r'[^0-9,]', '', line)
    doc_id, doc = line.split()
    print >> f2, '%s\t%s' % (doc_id, doc)

