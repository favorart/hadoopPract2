#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import defaultdict
from itertools import groupby
from operator import itemgetter
import numpy as np
import sys
import os
import io

# mapper

for line in sys.stdin:
    if line.startswith('"'): continue
    print '\t'.join(line.strip().split(','))


