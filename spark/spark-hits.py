# /usr/local/spark/bin/pyspark
from pyspark import SparkContext

logFile = "$YOUR_SPARK_HOME/README.md"  # Should be some file on your system
sc = SparkContext("local", "HITS") #  'yarn-client'


# HITS
graph  = sc.textFile('spark_lenta_hits_graph')
adj_l  = graph.map( lambda line: line.strip().rstrip('\n').split("\t") )


# key:
#   v  = x[0]      int
# value:
#   h  = x[1][0]   int
#   a  = x[1][1]   int
#   ws = x[1][2]  [int]   # исходящие
#   us = x[1][3]  [int]   # входящие
adj_g   = adj_l.map(lambda x: (int(x[0]), (int(x[1]), int(x[2]), \
                              map(int, x[3].split(',')) if len(x[3])  else [], \
                              map(int, x[4].split(',')) if len(x) > 4 else [] )) )

# START ITERATIONS
for i in xrange(10):
    # adj_g = sc.pickleFile("spark-obj-HITS-step-" + str(i-1))
    
    # One iteration
    h_msgs = adj_g.flatMap(lambda x: [ (u, x[1][0]) for u in x[1][3] ]) # для каждой  входящей отправить h
    a_msgs = adj_g.flatMap(lambda x: [ (w, x[1][1]) for w in x[1][2] ]) # для каждой исходящей отправить а
    h_msgs1 = h_msgs.reduceByKey(lambda a,b: a + b)
    a_msgs1 = a_msgs.reduceByKey(lambda a,b: a + b)

    # join new values
    joined = h_msgs1.fullOuterJoin(a_msgs1)
    # key:
    #   v  = x[0] int
    # value:
    #   h = x[1][0] int
    #   a = x[1][1] int

    # join with graph structure
    joined1 = adj_g.leftOuterJoin(joined)
    # key:
    #   v      = x[0]  int
    # value:
    #   struct = x[1][0] ( h (int), a (int), ws ([int]), us ([int]) )
    #   new_ha = x[1][1] ( h (int), a (int) )

    adj_g1 = joined1.map(lambda x: (x[0], ( x[1][1][0] if x[1][1] and x[1][1][0] else 0, \
                                            x[1][1][1] if x[1][1] and x[1][1][1] else 0, \
                                            x[1][0][2],   x[1][0][3]) ))
    # key:
    #   v  = x[0]      int
    # value:
    #   h  = x[1][0]   int
    #   a  = x[1][1]   int
    #   ws = x[1][2]  [int]
    #   us = x[1][3]  [int]

    adj_g1.saveAsPickleFile("spark-obj-HITS-step-" + str(i))
    # adj_g1.saveAsTextFile("spark-HITS-step-" + str(i))
    adj_g = adj_g1


# RESULT
result = adj_g.takeOrdered(30, lambda x: -(x[1][0] + x[1][1]))
# result.saveAsTextFile("spark-HITS-result")
print result

