# -*- coding: utf-8 -*-
"""
Created on Sun Nov 19 17:47:26 2017

@author: srema
"""


Entities = ["Obama", "Trump", "Clinton", "Bush", "Reagan"]

for ent in range(len(Entities)):
    print ('curl "http://10.149.0.127:9200/freebase/label/_search?q=' + Entities[ent] + '"')
     