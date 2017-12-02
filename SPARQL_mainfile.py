import traceback
from pyspark.context import SparkContext
import sys
from nltk.tag import StanfordNERTagger
import shutil
from nltk.tokenize import word_tokenize
import re
sys.path.append('/home/wdps1703/lib/python2.7/site-packages')
import requests
import json
import collections, math

def ner_stanford((x, text), st):
    tokenized_text = word_tokenize(text.decode('UTF-8'))
    classified_text = st.tag(tokenized_text)
    output = []
    for tup in classified_text:
        if tup[1] != 'O':
            output.append(tup)
    return ((x,output))

# defines which tags are excluded from the HTML file
def visible(element):
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
        print("Something went wrong with the archive entry")

    return html_pages_array

def create_output((x, text)):
    output = []
    text = list(set(text))
    for (entity, tag) in text:
        output.append(str(x)+","+entity+","+tag)
    return output


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

stanford_rdd = rdd_html_cleaned.map(lambda (x, y): ner_stanford((x, y), st))
# Extract named entities
text_rdd = stanford_rdd.flatMap(lambda (x,y):create_output((x,y)))

print(text_rdd.collect())




ELASTICSEARCH_URL = 'http://10.149.0.127:9200/freebase/label/_search'
TRIDENT_URL = 'http://10.141.0.11:8082/sparql'

query = # tokens obtained 

print('Searching for "%s"...' % query)
response = requests.get(ELASTICSEARCH_URL, params={'q': query, 'size':100})

ids = set()
labels = {}
scores = {}

if response:
    response = response.json()
    for hit in response.get('hits', {}).get('hits', []):
        freebase_id = hit.get('_source', {}).get('resource')
        label = hit.get('_source', {}).get('label')
        score = hit.get('_score', 0)
        ids.add( freebase_id )
        scores[freebase_id] = max(scores.get(freebase_id, 0), score)
        labels.setdefault(freebase_id, set()).add( label )

print('Found %s results.' % len(labels))

prefixes = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX fbase: <http://rdf.freebase.com/ns/>
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wds: <http://www.wikidata.org/entity/statement/>
PREFIX wdv: <http://www.wikidata.org/value/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
"""
same_as_template = prefixes + """
SELECT DISTINCT ?same WHERE {
    ?s owl:sameAs %s .
    { ?s owl:sameAs ?same .} UNION { ?same owl:sameAs ?s .}
}
"""
po_template = prefixes + """
SELECT DISTINCT * WHERE {
    %s ?p ?o.
}
"""

print('Counting KB facts...')
facts  = {}
for i in ids:
    response = requests.post(TRIDENT_URL, data={'print': False, 'query': po_template % i})
    if response:
        response = response.json()
        n = int(response.get('stats',{}).get('nresults',0))
        print(i, ':', n)
        sys.stdout.flush()
        facts[i] = n

def get_best(i):
    return math.log(facts[i]) * scores[i]

print('Best matches:')
for i in sorted(ids, key=get_best, reverse=True)[:3]:
    print(i, ':', labels[i], '(facts: %s, score: %.2f)' % (facts[i], scores[i]) )
    sys.stdout.flush()
    response = requests.post(TRIDENT_URL, data={'print': True, 'query': same_as_template % i})
    if response:
        response = response.json()
        for binding in response.get('results', {}).get('bindings', []):
            print(' =', binding.get('same', {}).get('value', None))



