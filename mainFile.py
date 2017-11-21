# -*- coding: utf-8 -*-
from pyspark.context import SparkContext
from html2text import HTML2Text
from warcio.archiveiterator import ArchiveIterator
from bs4 import BeautifulSoup
import re
import sys


# Function to traverse the chunked tree in NLTK
def traverseTree((x, fullDoc)):
    outList = {}
    for tree in fullDoc:
        for chunk in tree:
            if hasattr(chunk, 'label'):
                outList[' '.join(c[0] for c in chunk)] = chunk.label()
    return (x, outList)


# Function to tokenize a text
def ner((x, text)):
    import nltk
    sentences = nltk.sent_tokenize(text)
    sentences = [nltk.word_tokenize(sent) for sent in sentences]
    sentences = [nltk.pos_tag(sent) for sent in sentences]
    chunks = [nltk.ne_chunk(sent) for sent in sentences]
    return (x, chunks)


# defines which tags are excluded from the HTML file
def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element.encode('utf-8'))):
        return False
    return True



def decode(x, record_attribute):
    html_pages_array = []
    _, payload = x
    wholeTextFile = ''.join([c.encode('utf-8') for c in payload])
    wholeTextFile = "WARC/1.0"+wholeTextFile
    from cStringIO import StringIO
    stream = StringIO(wholeTextFile)
    try:
        for record in ArchiveIterator(stream):

            # if the record type is a response (which is the case for html page)

            if record.rec_type == 'response':
                # check if the response is http
                if record.http_headers != None:
                    # Get the WARC-RECORD-ID
                    record_id = record.rec_headers.get_header(record_attribute)
                    print (record_id)
                    # Get the HTML
                    h = HTML2Text()
                    # Clean up the HTML using BeautifulSoup
                    html = record.content_stream().read()
                    soup = BeautifulSoup(html, "html5lib")
                    data = soup.findAll(text=True)
                    result = filter(visible, data)

                    result2 = ';'.encode('utf-8').join(result)
                    result2 = ' '.join(result2.split())
                    # Build up the resulting list.
                    # result2 = re.sub(r'[\?\.\!]+(?=[\?\.\!])', '.', result2)
                    html_pages_array.append((record_id, result2.encode('utf-8')))
    except Exception:
        print ("Something is wrong with this entry.")

    return html_pages_array


record_attribute = sys.argv[1]#"WARC-Record-ID"
in_file = sys.argv[2]#"/home/kevin/Documents/WDPS/wdps2017/CommonCrawl-sample.warc.gz"
# We read one WARC file. This list will contain tuples consisting of the WARC-Record-ID and the cleaned up HTML

# Create Spark Context -- Remove this when running on cluster
sc = SparkContext.getOrCreate()

rdd_whole_warc_file = rdd = sc.newAPIHadoopFile(in_file,
    "org.apache.hadoop.mapreduce.lib.input.TextInputFormat",
    "org.apache.hadoop.io.LongWritable",
    "org.apache.hadoop.io.Text",
    conf={"textinputformat.record.delimiter": "WARC/1.0"})

rdd_html_cleaned = rdd_whole_warc_file.flatMap(lambda x: decode(x, record_attribute))

print(rdd_html_cleaned.collect())
chunked_rdd = rdd_html_cleaned.map(lambda (x, y): ner((x, y)))
# Extract named entities
named_entity_rdd = chunked_rdd.map(lambda (x, y): traverseTree((x, y)))
print(named_entity_rdd.collect())
