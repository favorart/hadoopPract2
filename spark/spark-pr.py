# /usr/local/spark/bin/pyspark
from pyspark import SparkContext

logFile = "$YOUR_SPARK_HOME/README.md"  # Should be some file on your system
sc = SparkContext("local", "PAGE-RANK")


# PAGE-RANK
graph  = sc.textFile('spark_lenta_pr_graph')
adj_l  = graph.map(lambda line: line.strip().rstrip('\n').split("\t"))


# key:
#   v  = x[0] int
# value:
#   PR = x[1][0] float
#   ws = x[1][1] [int]
adj_p  = adj_l.map(lambda line: (int(line[0]), (float(line[1]), \
                                 map(int, line[2].split(',')) if len(line) > 2 else [] ) ))

# ---обработка висячих вершин---
number = adj_p.count()
bcNumber = sc.broadcast(number)
# ------------------------------

# START ITERATIONS
for i in xrange(10):
    # adj_p = sc.pickleFile("spark-obj-PR-step-" + str(i-1))

    # One iteration
    iter   = adj_p.flatMap(lambda el: [(to, el[1][0] / len(el[1][1])) for to in el[1][1] ] # )
                                       # ---обработка висячих вершин------------------
                                       if len(el[1][1]) else [((bcNumber + 1), el[1][0] / bcNumber)] )
    # key:
    #  w   = x[0] int
    # value:
    #  nPR = x[1] (float)

    reduce = iter.reduceByKey(lambda a,b: a + b)
    # ---обработка висячих вершин---
    hangValRDD = reduce.filter(lambda x: x[0] == (bcNumber + 1))
    hangVal = hangValRDD.collect()
    if len(hangVal) != 1:
        print hangVal
        raise ValueError
    bcHangVal = sc.broadcast(hangVal[0])
    reduce = reduce.map(lambda x: (x[0], x[1] + bcHangVal))
    # ------------------------------
    joined = adj_p.leftOuterJoin(reduce)
    # key:
    #   v      = x[0] int
    # value:
    #   struct = x[1][0] (float, [int]) = (PR, ws)
    #   nPR    = x[1][1]  float

    adj_p1 = joined.map(lambda x: (x[0], (0.15 + 0.85 * x[1][1]  if x[1][1]
                                   else   0.15, x[1][0][1])))
    # key:
    #   v  = x[0] int
    # value:
    #   PR = x[1][0] float
    #   ws = x[1][1] [int]

    adj_p1.saveAsPickleFile("spark-obj-PR-step-" + str(i))
    # adj_p1.saveAsTextFile("spark-PR-graph-step-" + str(i))
    adj_p = adj_p1
    # adj_p.take(1)

# RESULT
result = adj_p.takeOrdered(30, key=lambda x: -x[1][0])
# result.saveAsTextFile("spark-PR-result")
print result

