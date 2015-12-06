#!/bin/sh

INPUT='/data/sites/lenta.ru/all/docs-*.txt'
OUTPUT='is5_all_lenta_map'

hadoop fs -rm -r ${OUTPUT}
hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
    -D mapreduce.job.name='is5_map' \
    -file mapper.py bs123.zip \
    -mapper  'python mapper.py' \
    -input ${INPUT} \
    -output ${OUTPUT}


INPUT='is5_all_lenta_map/part-*'
OUTPUT='is5_all_lenta_2sides_graph'

hadoop fs -rm -r ${OUTPUT}
hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
    -D mapreduce.job.name='is5_graph' \
    -file map.py reducer.py bs123.zip \
    -mapper  'python map.py' \
    -reducer 'python reducer.py' \
    -numReduceTasks 10  \
    -input ${INPUT} \
    -output ${OUTPUT}

hadoop fs -get is5_all_lenta_2sides_graph
bash local.sh