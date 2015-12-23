#!/usr/bin python
# -*- coding: utf-8 -*-

import codecs
import sys
sys.path.insert(0, './spark/')
import re


fn_urls     = sys.argv[1] if len(sys.argv) > 1 else 'spark/urls.txt'
fn_new_urls = sys.argv[2] if len(sys.argv) > 2 else 'spark/new_urls.txt'
fn_results = [  ('result-hits.txt', 'hits') ] # ('result-pr.txt', 'pr'),


with codecs.open(fn_urls, 'r', encoding='utf-8') as f_urls:
    splts = [ line.rstrip('\n').split(u'\t') for line in f_urls ]
    urls = dict( (int(splt[0]), splt[1]) for splt in splts if len(splt) >= 2 )
print fn_urls


with codecs.open(fn_new_urls, 'r', encoding='utf-8') as f:
    splts = [ line.rstrip('\n').split(u'\t') for line in f ]
    new_urls = dict( (int(splt[0]), splt[1]) for splt in splts if len(splt) >= 2 )
print fn_new_urls


print '\n'
for fn, op in fn_results:
    with codecs.open(fn, 'r', encoding='utf-8') as f_pr:
        for line in f_pr:

            m = re.search(ur'\s*[(]([0-9]+L?)\s*,\s*[(]([0-9.]+)L?,\s*([0-9.]+)?L?', line)
            # print line, m.group(1) if m else '-'

            if m:
                id, pr_h, a = int(m.group(1)), float(m.group(2)), float(m.group(3)) if m.group(3) else ''
                print '%d %.3f %s\t%s' % (id, pr_h, a, urls[id] if (id in urls) else \
                                            (new_urls[id] if (id in new_urls) else ''))

    print '\n%s\n' % fn


