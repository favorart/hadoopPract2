#!/usr/bin python
# -*- coding: utf-8 -*-

import codecs
import sys
import re

for line in sys.stdin:

    m = re.search(ur'[(]([0-9]+)\s*,\s*[(]([0-9.]+),\s*([0-9.]+)?', line)
    # print line, m.group(1) if m else '-'

    if m:
        if m.group(3):
            id, h, a = int(m.group(1)), int(m.group(2)), int(m.group(3))
            print '%d\t%d\t%d' % (id, h, a)
        else:
            id, pr = int(m.group(1)), m.group(2)
            print '%d\t%s' % (id, pr)
