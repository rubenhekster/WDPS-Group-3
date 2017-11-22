import traceback
from pyspark.context import SparkContext
import sys
from nltk.tag import StanfordNERTagger


def ner_stanford((x, text), st):

    from nltk.tokenize import word_tokenize

    tokenized_text = word_tokenize(text)
    classified_text = st.tag(tokenized_text)
    output = []
    for tup in classified_text:
        if tup[1] != 'O':
            output.append(tup)
    print ((x,output))

# defines which tags are excluded from the HTML file
def visible(element):
    import re
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', element.encode('UTF-8')):
        return False
    return True


def decode(x, record_attribute):
    html_pages_array = []
    _, payload = x
    wholeTextFile = ''.join([c.encode('utf-8') for c in payload])
    wholeTextFile = "WARC/1.0 " + wholeTextFile

    from cStringIO import StringIO
    from warcio.archiveiterator import ArchiveIterator
    from html2text import HTML2Text
    from bs4 import BeautifulSoup
    stream = StringIO(wholeTextFile)
    try:
        for record in ArchiveIterator(stream):
            # if the record type is a response (which is the case for html page)

                if record.rec_type == 'response':
                    # check if the response is http
                    if record.http_headers != None:
                        # Get the WARC-RECORD-ID
                        record_id = record.rec_headers.get_header(record_attribute)
                        # Clean up the HTML using BeautifulSoup
                        html = record.content_stream().read()
                        soup = BeautifulSoup(html, "html5lib")
                        data = soup.findAll(text=True)
                        result = filter(visible, data)
                        result2 = ' '.join(result)
                        result2 = ' '.join(result2.split()).encode('utf-8')
                        # Build up the resulting list.
                        # result2 = re.sub(r'[\?\.\!]+(?=[\?\.\!])', '.', result2)
                        html_pages_array.append((record_id, result2))
    except Exception:
        traceback.print_exc()

    return html_pages_array


record_attribute = sys.argv[1]  # "WARC-Record-ID"
in_file = sys.argv[2]  # "/home/kevin/Documents/WDPS/wdps2017/CommonCrawl-sample.warc.gz"
stanford = sys.argv[3] # https://nlp.stanford.edu/software/stanford-ner-2017-06-09.zip
# We read one WARC file. This list will contain tuples consisting of the WARC-Record-ID and the cleaned up HTML

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

chunked_rdd = rdd_html_cleaned.map(lambda (x, y): ner_stanford((x, y), st))
# Extract named entities

print(chunked_rdd.collect())
