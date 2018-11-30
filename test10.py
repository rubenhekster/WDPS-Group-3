#import traceback
from pyspark.context import SparkContext
#import sys
from nltk.tag import StanfordNERTagger
#import shutil
from nltk.tokenize import word_tokenize
import nltk
import re
import os
#import pdb
#import warc

# nltk.download() # Use only if not yet installed

def get_array(input):

    identifier = []
    html_text = []

    for i in range(len(input)):
        identifier.append(input[i][0])
        html_text.append(input[i][1])

    return identifier, html_text


def ner_stanford(input, st):

    x, text = get_array(input)

    print('test')
    output = []
    for i in range(len(text)):
        tokenized_text = word_tokenize(text[i])
        classified_text = st.tag(tokenized_text)

        for tup in classified_text:
            if tup[1] != 'O':
                output.append(tup)

    return x, output


# defines which tags are excluded from the HTML file
def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', element): #.encode('utf-8')):
        return False
    return True


def decode(x, record_attribute):
    html_pages_array = []

    # identifier = []
    # html_text = []

    _, payload = x
    # payload = (payload.encode('utf-8'))

    wholeTextFile = ''.join([c for c in payload])
    wholeTextFile = "WARC/1.0 " + wholeTextFile
    wholeTextFile = wholeTextFile.encode('utf-8')
    # print(wholeTextFile)

    from io import BytesIO
    from warcio.archiveiterator import ArchiveIterator

    #from html2text import HTML2Text
    from bs4 import BeautifulSoup
    #import html5lib

    stream = BytesIO(wholeTextFile)

    list_error = []
    try:
        for record in ArchiveIterator(stream):

            # if the record type is a response (which is the case for html page)
            list_error.append('1')
            if record.rec_type == 'response':
                list_error.append('2')
                # check if the response is http
                if record.http_headers != None:
                    list_error.append('3')
                    # Get the WARC-RECORD-ID
                    record_id = record.rec_headers.get_header(record_attribute)
                    list_error.append('4')
                    # Clean up the HTML using BeautifulSoup
                    html = record.content_stream().read()
                    soup = BeautifulSoup(html, "html5lib")
                    data = soup.findAll(text=True)#.encode()
                    list_error.append('5')
                    result = filter(visible, data)
                    list_error.append('5.1')
                    result2 = ' '.join(result)
                    list_error.append('5.2')
                    result2 = ' '.join(result2.split())
                    list_error.append('6')
                    # Build up the resulting list.
                    #result2 = re.sub(r'[\?\.\!]+(?=[\?\.\!])', '.', result2)
                    #result2 = result2.encode('utf-16')
                    #result2 = result2.encode("utf-8")
                    list_error.append('7')
                    result2 = result2.encode('ascii', errors="ignore").decode('ascii')
                    list_error.append('7.1')
                    if result2 != '' and isinstance(result2, str):
                        html_pages_array.append([record_id, result2])
                        # identifier.append(record_id)
                        # html_text.append(result2)
                        list_error.append('8')

    except Exception:
        print("Something went wrong with the archive entry")
        print(list_error)


    # for i in range(len(html_pages_array)):
    # #     print(type(html_pages_array[i]))
    #     iden
    #     print('num 1', type(html_pages_array[i][0]))
    #     print('num 2', type(html_pages_array[i][1]))

        #html_pages_array[i] = html_pages_array[i].encode
    # print(len(html_pages_array))
    # html_pages_array[25]
    return html_pages_array #identifier, html_text


def create_output(x, text):
    output = []
    text = list(set(text))
    for (entity, tag) in text:
        output.append(str(x) + "," + entity + "," + tag)
    return output



java_path = "C:/Program Files/Java/jdk1.8.0_191/bin/java.exe"
os.environ['JAVAHOME'] = java_path

record_attribute = "WARC-Record-ID"
in_file = "C:/Users/klm85310/Documents/WDPS/sample.warc.gz"
stanford = 'C:/Users/klm85310/Documents/WDPS/stanford-ner-2017-06-09/stanford-ner-2017-06-09'

# Create Spark Context -- Remove this when running on cluster
sc = SparkContext.getOrCreate()
st = StanfordNERTagger(stanford + '/classifiers/english.all.3class.distsim.crf.ser.gz',
                       stanford + '/stanford-ner.jar',
                       encoding='utf-8')

rdd_whole_warc_file = rdd = sc.newAPIHadoopFile(in_file,
                                                "org.apache.hadoop.mapreduce.lib.input.TextInputFormat",
                                                "org.apache.hadoop.io.LongWritable",
                                                "org.apache.hadoop.io.Text",
                                                conf={"textinputformat.record.delimiter": "WARC/1.0"})

rdd_html_cleaned = rdd_whole_warc_file.flatMap(lambda x: decode(x, record_attribute))

print("step 2")



stanford_rdd = rdd_html_cleaned.map(lambda x: ner_stanford(x, st))
# Extract named entities
# text_rdd = stanford_rdd.flatMap(lambda x ,y : create_output(x,y))
#rdd_html_cleaned.saveAsTextFile("sample_text.txt")
#full_text = rdd_html_cleaned.collect()

print(stanford_rdd.collect())
print('Done')

# def main():
#
#     f = warc.open("sample.warc.gz")
#     for record in f:
#
#         record_attribute = "WARC-Record-ID"
#         in_file = record #"C:/Users/klm85310/Documents/WDPS/sample.warc.gz" #sys.argv[2]  # "C:/Users/klm85310/Documents/WDPS/sample.warc.gz"
#         stanford = 'https://nlp.stanford.edu/software/stanford-ner-2017-06-09.zip'
#
#         decode(in_file, record_attribute)
# # We read one WARC file. This list will contain tuples consisting of the WARC-Record-ID and the cleaned up HTML
#
# if __name__ == "__main__":
#     main()
#     print("Done")
