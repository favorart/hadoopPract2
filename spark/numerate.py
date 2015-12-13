#!/usr/bin python
# -*- coding: utf-8 -*-

import pickle
import codecs
import sys
import re
import os


# type reduced | python numerate.py "C:\data\lenta.ru\all\urls.txt" "new_urls.txt" | sort > numerated
fn_urls     = sys.argv[1] if len(sys.argv) > 1 else 'urls.txt'
fn_new_urls = sys.argv[2] if len(sys.argv) > 2 else 'new_urls.txt'


re_norm_url = re.compile(ur'^https?://[^/]*lenta\./|/?\r?\n?$')
def normalize(url):
    """ Remove the main domain from the link address
           and last slesh or new-line-char if it is
    """
    normed = re_norm_url.sub(u'', url)
    return normed if len(normed) else 'lenta'


def numerate(url, urls, new_urls):
    """ Replace the http-links by the ids of documents """
    # if it is already enumerated
    if  not len(url) or unicode(url).isdigit():
        return url

    if u'h' not in url: print >>sys.stderr, url
    # -----------------------------------
    url = normalize(url)

    if  url in urls:
        return unicode(urls[url])

    id = unicode(len(urls))
    new_urls.append( (id, url) )
    urls[url] = id
    # -----------------------------------
    return id


if not os.path.exists('urls.pkl'):
    
    with codecs.open(fn_urls, 'r', encoding='utf-8') as f_urls:
        splts = [ line.split(u'\t') for line in f_urls ]
        urls = dict( (normalize(url), id) for id, url in splts )

    with open('urls.pkl', 'w') as f:
        pickle.dump(urls,f)
else:
    with open('urls.pkl', 'r') as f:
        urls = pickle.load(f)


new_urls = []
# Используем unicode в стандартных потоках io
sys.stdin  = codecs.getreader('utf-8')(sys.stdin)
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)  # open('gr', 'w'))# 
sys.stderr = codecs.getwriter('utf-8')(sys.stderr)

# codecs.open('spark/is5_all_lenta_2sides_graph/part-00000', 'r', encoding='utf-8'): # 
for line in sys.stdin:
    splt = line.rstrip('\n').split(u'\t')

    if  len(splt) == 3:
        v, PR,  wlinks = splt
        w_urls = wlinks.split(u'|')

        v = numerate(v, urls, new_urls)

        ws = [ numerate(url, urls, new_urls) for url in w_urls ]
        print u'%s\t%s\t%s' % ( v, PR, u','.join(ws) )

    elif  len(splt) == 5:
        v, h, a, w_links, u_links = splt
        w_urls = w_links.split(u'|')
        u_urls = u_links.split(u'|')

        v = numerate(v, urls, new_urls)

        ws = [ numerate(url, urls, new_urls) for url in w_urls ]
        us = [ numerate(url, urls, new_urls) for url in u_urls ]
        print u'%s\t%s\t%s\t%s\t%s' % (v, h, a, u','.join([ w for w in ws if len(w) ]), 
                                                u','.join([ u for u in us if len(u) ]) )


# Save the new found urls enumerated
with codecs.open(fn_new_urls, 'a', encoding='utf-8') as f:
    print >>f, u''.join([ u'%s\t%s\n' % (id,url) for id,url in new_urls ])

