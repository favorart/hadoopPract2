#!/usr/bin python
# -*- coding: utf-8 -*-

from base64 import b64encode
from operator import itemgetter

import codecs
import sys
import re

import zipimport
importer = zipimport.zipimporter('bs123.zip')


# Используем unicode в стандартных потоках io
sys.stdin  = codecs.getreader('utf-8')(sys.stdin)
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
sys.stderr = codecs.getwriter('utf-8')(sys.stderr)

for line in sys.stdin:

    splt = line.strip().split('\t')

    if len(splt) == 1:

        print u'%s\t' % (line)
        del splt

