import requests
from warcio.archiveiterator import ArchiveIterator
from html2text import HTML2Text
handler = HTML2Text()
import html5lib


def warcToText(url):
# request the url/warc.gz file
    resp = requests.get(url, stream=True)
    # iterate through the archive
    for record in ArchiveIterator(resp.raw, arc2warc=True):
        # if the record type is a response (which is the case for html page)
        if record.rec_type == 'response':
            # check if the response is http
            if record.http_headers != None:
                # if the http header is one of the following
                if ((record.http_headers.get_header('Content-Type') =='text/html') |(record.http_headers.get_header('Content-Type') == 'text/html; charset=UTF-8')\
                 | (record.http_headers.get_header('Content-Type') =='text/html; charset=utf-8')| (record.http_headers.get_header('Content-Type') =='text/html; charset=ISO-8859-1')\
                 | (record.http_headers.get_header('Content-Type') =='charset=iso-8859-1')):
                    # return the html page
                    html = record.content_stream().read()
                    # from html to plain text
                    html_parse = html5lib.parseFragment(html)
                    s = ''.join(html_parse.itertext())
                    print(s)

def main():
    reco = warcToText('https://archive.org/download/ExampleArcAndWarcFiles/IAH-20080430204825-00000-blackbook.warc.gz')


if __name__=='__main__':
    main()
