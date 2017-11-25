# -*- coding: utf-8 -*-
"""
Created on Sat Nov 25 13:38:33 2017

@author: Abdullah
"""

from elasticsearch import Elasticsearch
from pyspark.context import SparkContext
#from pyspark import SparkContext, SparkConf

sc = SparkContext()

print("Start")

es = Elasticsearch("http://10.149.0.127:9200")

rdd = sc.parallelize["Obama", "Trump", "Clinton", "Bush", "Reagan"]

#res = es.search(index="freebase", body={"query": {"match":{"label":x}}})

output = rdd.flatMap(lambda x: es.search(index="freebase", body={"query": {"match":{"label":x}}}))

print(output)

print("Done")