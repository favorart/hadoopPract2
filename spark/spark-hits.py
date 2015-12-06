# /usr/local/spark/bin/pyspark

# HITS
graph  = sc.textFile('spark_lenta_graph/part-*')

adj_l  = graph.map(lambda x: x.strip().split("\t"))
adj_l  = adj_l.filter(lambda x: len(x) == 5)

adj_l   = adj_l.map(lambda x: (int(x[0]), (int(x[1]), int(x[2]), \
                              map(int, x[3].split(',')), \
                              map(int, x[4].split(',')) )) )
# key:
#   v  = x[0]  int
# value:
#   h  = x[1]  int
#   a  = x[2]  int
#   ws = x[3]  [int]
#   us = x[4]  [int]

# it-1
h_msgs = adj_g.map(lambda x: [ (u, x[1]) for u in x[4] ])
a_msgs = adj_g.map(lambda x: [ (w, x[2]) for w in x[3] ])
h_msgs1 = h_msgs.reduceByKey(lambda a,b: a + b)
a_msgs1 = a_msgs.reduceByKey(lambda a,b: a + b)

joined = h_msgs1.join(a_msgs1)
# key:
#   v  = x[0] int
# value:
#   h = x[1][0] int
#   a = x[1][1] int

joined = adj_g.join(joined)
# key:
#   v      = x[0]  int
# value:
#   struct = x[1][0] ( h (int), a (int), ws ([int]), us ([int]) )
#   new_ha = x[1][1] ( h (int), a (int) )

adj_g1 = joined.map(lambda x: (x[0], x[1][1][0], x[1][1][1], x[1][0][2], x[1][0][3]))
# key:
#   v  = x[0]  int
# value:
#   h  = x[1]  int
#   a  = x[2]  int
#   ws = x[3]  [int]
#   us = x[4]  [int]

adj_g1.saveAsTextFile("spark_hits_graph_step1")

# RESULT
adj_g1.takeOrdered(30, lambda x: -(x[1] + x[2]))

