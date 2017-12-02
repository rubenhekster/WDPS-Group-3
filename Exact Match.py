from elasticsearch import Elasticsearch
from nltk.corpus import stopwords
import re
from collections import Counter

def Entity(Query, Before, After):
    Before_ = dict(Counter(Before))
    After_ = dict(Counter(After))
    maxBefore = Before_[max(Before_, key=lambda key: Before_[key])]
    maxAfter = After_[max(After_, key=lambda key: After_[key])]
    print("MaxB: ", maxBefore)
    if maxBefore > maxAfter:
        return max(Before_, key=lambda key: Before_[key]) + " " + Query
    else:
        return Query + " " + max(After_, key=lambda key: After_[key])
    

    

def main():
    File = open('Obama.txt','r').read().split()
    Query = "Obama"
    stop_words = set(stopwords.words("english"))
    Before = []
    After = []

    j = 0
    for i in range(len(File)):
        #File[i] = File[i].replace(" ","")
        #print(File[i])
        if File[i] == Query:
            #print("succes", File[i-1], File[i+1])
            try:
                if File[i-1] not in stop_words:
                    Before.append(File[i-1])
                if File[i+1] not in stop_words:
                    After.append(File[i+1])
                j = j+1
            except:
                pass

    


    Entity_ = Entity(Query, Before, After)
    print(Entity_)
    

if __name__ == '__main__':
    main()
    print("Done")
