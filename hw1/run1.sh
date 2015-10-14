#!/bin/sh
hadoop fs -rm -r aggregate

hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
	 -files mapper1.py \
	 -mapper 'mapper1.py 1' \
	 -reducer aggregate \
	 -input /data/patents/apat63_99.txt \
	 -output aggregate1

