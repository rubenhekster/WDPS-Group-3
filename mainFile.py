# -*- coding: utf-8 -*-
from pyspark.context import SparkContext
from html2text import HTML2Text
import gzip
from warcio.archiveiterator import ArchiveIterator
from bs4 import BeautifulSoup
import re


# Function to traverse the chunked tree in NLTK
def traverseTree((x, tree)):
    outList = {}
    for chunk in tree:
        if hasattr(chunk, 'label'):
            outList[' '.join(c[0] for c in chunk)] = chunk.label()
    return (x, outList)


# Function to tokenize a text
def ner((x, text)):
    import nltk
    return (x, nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(text))))


# defines which tags are excluded from the HTML file
def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element.encode('utf-8'))):
        return False
    return True


# We read one WARC file. This list will contain tuples consisting of the WARC-Record-ID and the cleaned up HTML
html_pages_array = []

# Opens the gzipped warc file.
with gzip.open('/home/kevin/Documents/WDPS/wdps2017/CommonCrawl-sample.warc.gz', 'rb') as stream:
    for record in ArchiveIterator(stream):
        # if the record type is a response (which is the case for html page)
        if record.rec_type == 'response':
            # check if the response is http
            if record.http_headers != None:
                # Get the WARC-RECORD-ID
                record_id = record.rec_headers.get_header('WARC-Record-ID')
                # Get the HTML
                h = HTML2Text()
                # Clean up the HTML using BeautifulSoup
                html = record.content_stream().read()
                soup = BeautifulSoup(html, "html5lib")
                data = soup.findAll(text=True)
                result = filter(visible, data)
                result2 = ''.join(result)
                # Build up the resulting list.
                html_pages_array.append((record_id, result2.encode('utf-8')))

# Create Spark Context
sc = SparkContext.getOrCreate()
# Parallelize the previously created list so it will work in Spark
documentRDD = sc.parallelize(html_pages_array)
# Chunk the text
chunked_rdd = documentRDD.map(lambda (x, y): ner((x, y)))
# Extract named entities
named_entity_rdd = chunked_rdd.map(lambda (x, y): traverseTree((x, y)))
print(named_entity_rdd.collect())
