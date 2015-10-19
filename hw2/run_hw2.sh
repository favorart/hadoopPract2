#!/bin/sh

INPUT='/data/patents/cite75_99.txt'
OUTPUT='PageRank_Step_0'

hadoop fs -rm -r ${OUTPUT}
hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
    -file mapper_p2.py reducer_p2.py \
    -mapper mapper_p2.py \
    -reducer reducer_p2.py \
    -input ${INPUT} \
    -output ${OUTPUT}

for ((i=1;i<=30;i++))
do
    INPUT=${OUTPUT}
    OUTPUT='PageRank_Step_'${i}

    hadoop fs -rm -r ${OUTPUT}
    hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
        -file mapper_hw2.py reducer_hw2.py \
        -mapper mapper_hw2.py \
        -reducer reducer_hw2.py \
        -input ${INPUT} \
        -output ${OUTPUT}
    hadoop fs -rm -r ${INPUT}

    hadoop fs -text ${OUTPUT}/part* | sort -k2,2nr | head > ${OUTPUT}_top.txt
done
