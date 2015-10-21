from collections import defaultdict
from itertools import groupby
from operator import itemgetter
import sys


# reducer
dic = defaultdict(list)
for line in sys.stdin: 
	line = line.strip()
	doc_id, doc = line.split()
	dic[doc_id].append(doc)

for doc_id,docs in dic.items():
	print '%s\tpr=0.15\t[%s]' % ( doc_id, ','.join(docs) )

