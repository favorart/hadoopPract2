# PAGE-RANK
graph  = sc.textFile('spark_lenta_graph/part-*')

adj_l  = graph.map(lambda line: line.split("\t"))
adj_l  = adj_l.filter(lambda x: len(x) == 3)

# ITER #1
adj_p  = adj_l.map(lambda line: (int(line[0]), (float(line[1]), [ int(el) for el in line[2].split(',')) ]))
# key:
#   v  = x[0] int
# value:
#   PR = x[1][0] float
#   ws = x[1][1] [int]

iter   = adj_p.flatMap(lambda el: [(to, el[1][0]/len(el[1][1])) for to in el[1][1] ])
# key:
#  w   = x[0] int
# value:
#  nPR = x[1] (float)

reduce = iter.reduceByKey(lambda a,b: a+b)
joined = adj_p.join(reduce)
# key:
#   v      = x[0] int
# value:
#   struct = x[1][0] (float, [int]) = (PR, ws)
#   nPR    = x[1][1]  float

adj_p1 = joined.map(lambda x: (x[0], x[1][1], x[1][0][1]))
# key:
#   v  = x[0] int
# value:
#   PR = x[1][0] float
#   ws = x[1][1] [int]

# adj_p1.take(1)
adj_p1.saveAsTextFile("spark_pr_graph_step1")

# RESULT
adj_p1.takeOrdered(30, key=lambda x: -x[1])