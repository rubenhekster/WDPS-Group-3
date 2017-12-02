import operator
from nltk.corpus import stopwords
from collections import Counter
from math import log
import numpy as np

def Hamming(str1, str2):

    str1_ = str1
    str2_ = str2
    
    if str1 > str2:
        dif = len(str1) - len(str2)
        for i in range(dif):
            str2_ = str2_ + "0"
    elif str1 < str2:
        dif = len(str2) - len(str1)
        for i in range(dif):
            str1_ = str1_ + "0"
        
    #print(str1_, str2_)

    ne = operator.ne
    return sum(map(ne, str1_, str2_))

def GetDistance(str1, str2):
    Dist = []
    
    for i in range(len(str2)):
        Dist.append(Hamming(str1, str2[i][0]))
      
    Dict = dict((x, y) for x, y in str2) #+ np.transpose(Dist) #+     

    i = 0
    for key, val in Dict.items():
        NewDict = {key : [val, Dist[i]]}
        i = i + 1

##    Best_Match = sorted(NewDict.items(), key=operator.itemgetter(2))
    return(NewDict)

        
def Sum(File):
    Sum = 0
    for key, value in File.items():
        Sum = Sum + int(value)

    return Sum

def main():
    

#pop + hamming
    File = open('Obama.txt','r').read().split()
    Query = "Obama"
    stop_words = set(stopwords.words("english"))

    for i in range(len(File)):
        try:
            if File[i] in stop_words:
                
                File.remove(File[i])
                
        except:
            pass
        
    File_ = Counter(File)
    Total = Sum(File_)

    for key, value in File_.items():
        File_[key] = int(value)/Total
        #print(File_[key])
        #File_[j] = log(File_[j]) / Total
    
    Top100 =  File_.most_common(100)
    print(Top100)        
    print(GetDistance(Query, Top100))

if __name__ == '__main__':
    main()
    print("Done")
