#!/bin/sh

javac -d ./classes/ PageRankProg.java PageRank.java PageRankPrepare.java
jar -cvf PageRank.jar -C ./classes/ ./
hadoop jar PageRank.jar org.myorg.PageRankProg