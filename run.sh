#!/usr/bin/env bash

ATT=${1:-"WARC-Record-ID"}
INFILE=${2:-"hdfs:///user/bbkruit/CommonCrawl-sample.warc.gz"}
STANFORD=${3:-"/home/wdps1703/WDPS-Group-3/coreNLP/stanford-ner-2017-06-09"}


PYSPARK_PYTHON=/home/wdps1703/bin/python ~/spark-2.1.2-bin-without-hadoop/bin/spark-submit --master yarn mainFile.py $ATT $INFILE $STANFORD
