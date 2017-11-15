from pyspark.context import SparkContext
from nltk import word_tokenize, pos_tag, ne_chunk


def traverseTree(tree):
    outList = {}
    for chunk in tree:
        if hasattr(chunk, 'label'):
            outList[' '.join(c[0] for c in chunk)] = chunk.label()
    return outList


sentences = ["Donald John Trump (born June 14, 1946) is the 45th and current President of the United States, "
             "in office since January 20, 2017. Before entering politics, he was a businessman and television "
             "personality. Trump was born in the New York City borough of Queens. He earned an economics degree from "
             "the Wharton School of the University of Pennsylvania. A third-generation businessman, Trump followed in "
             "the footsteps of his grandmother Elizabeth and father Fred in running the family real estate company.",
             "Barack Hussein Obama II (US: /bəˈrɑːk huːˈseɪn oʊˈbɑːmə/ (About this sound listen) bə-RAHK hoo-SAYN "
             "oh-BAH-mə;[1][2] born August 4, 1961) is an American politician who served as the 44th President of the "
             "United States from 2009 to 2017. The first African American to assume the presidency in American "
             "history, he previously served in the U.S. Senate representing Illinois from 2005 to 2008 and in the "
             "Illinois State Senate from 1997 to 2004.",
             "Honolulu (/ˌhɒnəˈluːluː/;[6] Hawaiian pronunciation: [honoˈlulu]) is the capital and largest city of "
             "the U.S. state of Hawaii. It is an unincorporated part of and the county seat of the City and County of "
             "Honolulu on the island of Oahu.[a] The city is the main gateway to Hawaii and a major portal into the "
             "United States. The city is also a major hub for international business, military defense, as well as "
             "famously being host to a diverse variety of east-west and Pacific culture, cuisine, and traditions."]


sc = SparkContext.getOrCreate()
sentences_rdd = sc.parallelize(sentences)
chunked_rdd = sentences_rdd.map(lambda x: ne_chunk(pos_tag(word_tokenize(x))))
named_entity_rdd = chunked_rdd.map(lambda x: traverseTree(x))

print(named_entity_rdd.collect())



