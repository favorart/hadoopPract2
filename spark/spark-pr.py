# /usr/local/spark/bin/pyspark
from pyspark import SparkContext

logFile = "$YOUR_SPARK_HOME/README.md"  # Should be some file on your system
sc = SparkContext("local", "PAGE-RANK")


# PAGE-RANK
graph  = sc.textFile('spark_lenta_pr_graph/part-*')
adj_l  = graph.map(lambda line: line.strip().rstrip('\n').split("\t"))
adj_l  = adj_l.filter(lambda x: len(x) == 3)


# key:
#   v  = x[0] int
# value:
#   PR = x[1][0] float
#   ws = x[1][1] [int]
adj_p  = adj_l.map(lambda line: (int(line[0]), (float(line[1]), \
                                 map(int, line[2].split(','))) ]))


# START ITERATIONS
for it in xrange(10):
    # adj_g = sc.pickleFile("spark-obj-PR-step-" + str(i-1))

    # One iteration
    iter   = adj_p.flatMap(lambda el: [(to, el[1][0]/len(el[1][1])) for to in el[1][1] ])
    # key:
    #  w   = x[0] int
    # value:
    #  nPR = x[1] (float)

    reduce = iter.reduceByKey(lambda a,b: a + b)
    joined = adj_p.fullOuterJoin(reduce)
    # key:
    #   v      = x[0] int
    # value:
    #   struct = x[1][0] (float, [int]) = (PR, ws)
    #   nPR    = x[1][1]  float

    adj_p1 = joined.map(lambda x: (x[0], x[1][1] if x[1][1] else 0.15, x[1][0][1]))
    # key:
    #   v  = x[0] int
    # value:
    #   PR = x[1][0] float
    #   ws = x[1][1] [int]

    # adj_p1.take(1)
    adj_p1.saveAsTextFile("spark_PR_graph_step" + str(i))
    adj_g1.saveAsPickleFile("spark-obj-PR-step-" + str(i))
    adj_p = adj_p1

# RESULT
result = adj_p.takeOrdered(30, key=lambda x: -x[1])
result.saveAsTextFile("spark-HITS-result")

