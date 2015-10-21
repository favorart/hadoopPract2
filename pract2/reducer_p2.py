from itertools import groupby
from operator import itemgetter
import sys

# reducer
for doc_id, group in groupby((line.strip().split('\t') for line in sys.stdin), itemgetter(0)):
    docs = set()
    for id, doc in group:
        docs.add(doc)
    print '%s\tpr=0.15\t[%s]' % ( doc_id, ','.join(docs) )
