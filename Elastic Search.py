# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 19:47:31 2017

@author: srema
"""

from elasticsearch import Elasticsearch

#Elasticsearch.download()

es = Elasticsearch("http://10.149.0.127:9200")

#res = es.search(index="freebase", body={"query": {"match_all":{}}})

query = ["Obama", "Trump", "Clinton", "Bush", "Reagan"]

res = es.search(index="freebase", body={"query": {"match_all":{"obama"}}})

#res = es.search(index="freebase", body={"query": {"match":{"label":"obama"}}})
print(res)
