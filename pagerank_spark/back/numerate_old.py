#!/usr/bin python
# -*- coding: utf-8 -*-

import codecs
import sys
import re


re_norm_url = re.compile(ur'^https?://[^/]*lenta\./|/?\r?\n?$')
def normalize(url):  return re_norm_url.sub(u'', url)


fn_urls = sys.argv[1]
with open(fn_urls, 'r') as f_urls:
    splts = [ line.strip().rstrip('\n').split('\t') for line in f_urls.readlines() ]
    urls = dict( (normalize(url), id) for id, url in splts )


new_links = []
# Используем unicode в стандартных потоках io
sys.stdin  = codecs.getreader('utf-8')(sys.stdin)
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
sys.stderr = codecs.getwriter('utf-8')(sys.stderr)

# type reduced | python numerate.py "C:\data\lenta.ru\all\urls.txt" "new_urls.txt" | sort > numerate
for line in sys.stdin:
    splt = line.strip().split('\t')

    if  len(splt) == 3:
        id, PR, third = splt
        links = third.split('|')

        ids = []
        for link in links:
            url = normalize(link)
            if  url in urls:
                ids.append( str(urls[url]) )
            else:
                ids.append( str(len(urls)) )

                new_links.append( (len(urls), link) )
                urls[url] = len(urls)

        # print >>sys.stderr, ids
        print '%s\t%s\t%s' % ( id, PR, ','.join(ids) )

    elif  len(splt) == 2:
        link, id = splt
        url = normalize(link)
        if  url in urls:
            u_id = str(urls[url])
        else:
            u_id = str(len(urls))

            new_links.append( (len(urls), link) )
            urls[url] = len(urls)

        print '%s\t%s' % ( u_id, id )


fn_new_urls = sys.argv[2]
with open(fn_new_urls, 'w') as f:
    for id, link in new_links:
        print >>f, id, link

