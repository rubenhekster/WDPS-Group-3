import operator
from nltk.corpus import stopwords

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


    ne = operator.ne
    return sum(map(ne, str1_, str2_))

def GetDistance(str1, str2):
    List = []
    for i in range(len(str2)):
        List.append([str2[i], Hamming(str1, str2[i])])

    return List
        
def main():
    
    File = open('Obama.txt','r').read().split()
    Query = "Obama"
    stop_words = set(stopwords.words("english"))

    for i in range(len(File)):
        try:
            if File[i] in stop_words:                
                File.remove(File[i])                
        except:
            pass

    List = GetDistance(Query, File)
    Dict = dict((x, y) for x, y in List)
    list_key_value = [ [k,v] for k, v in dict.items() ]
    Top100 = sorted(Dict.items(), key=lambda Dict: Dict[1])
    # To be continued ...
    print(Top100)
        
if __name__ == '__main__':
    main()
    print("Done")
