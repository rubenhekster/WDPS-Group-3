import nltk, string
from sklearn.feature_extraction.text import TfidfVectorizer
import operator
from sklearn.metrics import jaccard_similarity_score

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
        
    print(str1, "|", str2)

    ne = operator.ne
    return sum(map(ne, str1_, str2_))




def cosine_sim(text1, text2):
    tfidf = TfidfVectorizer().fit_transform([text1, text2])
    return ((tfidf * tfidf.T).A)[0,1]


##
def GetDistance(str1, str2):

    for i in range(len(str2)):
        print("Hamming Distance: ", Hamming(str1, str2[i]))
        print("Cosine Similarity: ", cosine_sim(str1, str2[i]))
        #print("Jaccard Similarty: ", jaccard_score(str1, str2[i]))

def main():


    str1 = "Obama was President of the USA"
    str2 = ["Barack was President of the USA",
            "Trump is the President of the United States",
            "Wyoming is a state of the USA",
            "Ted Cruz is the senator of Texas"]
    
    GetDistance(str1, str2)
    

if __name__ == '__main__':
    main()
    print("Done")
