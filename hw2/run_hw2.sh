#!/bin/sh

INPUT='/data/patents/cite75_99.txt'
OUTPUT='PageRank_python_Step_0'

hadoop fs -rm -r ${OUTPUT}
hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
    -D mapreduce.job.name=${OUTPUT} \
    -file mapper_p2.py reducer_p2.py \
    -mapper mapper_p2.py \
    -reducer reducer_p2.py \
    -input ${INPUT} \
    -output ${OUTPUT}

for ((i=1;i<=30;i++))
do
    INPUT=${OUTPUT}
    OUTPUT='PageRank_python_Step_'${i}

    hadoop fs -rm -r ${OUTPUT}
    hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
		-D mapreduce.job.name=${OUTPUT} \
        -file mapper_hw2.py reducer_hw2.py \
        -mapper mapper_hw2.py \
        -reducer reducer_hw2.py \
        -input ${INPUT} \
        -output ${OUTPUT}
    hadoop fs -rm -r ${INPUT}
done

