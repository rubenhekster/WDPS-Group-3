# -*- coding: utf-8 -*-
"""
Created on Sat Nov 25 18:28:52 2017

@author: Abdullah
"""

from pyspark import SparkConf
from pyspark.sql import SQLContext

conf = SparkConf().setAppName("ESTest")
sc = SparkContext(conf=conf)
sqlContext = SQLContext(sc)

q ="""{
  "query": {
    "filtered": {
      "filter": {
        "exists": {
          "field": "label"
        }
      },
      "query": {
        "match_all": {}
      }
    }
  }
}"""

es_read_conf = {
    "es.nodes" : "http://10.149.0.127",
    "es.port" : "9200",
    "es.resource" : "titanic/passenger",
    "es.query" : q
}

es_rdd = sc.newAPIHadoopRDD(
    inputFormatClass="org.elasticsearch.hadoop.mr.EsInputFormat",
    keyClass="org.apache.hadoop.io.NullWritable", 
    valueClass="org.elasticsearch.hadoop.mr.LinkedMapWritable", 
    conf=es_read_conf)

sqlContext.createDataFrame(es_rdd).collect()
