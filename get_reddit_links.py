import pycurl
import cStringIO
import pprint
from lxml.html import fromstring
import pdb

HEADER = [
            'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8;' +
            'rv:30.0) Gecko/20100101 Firefox/30.0',
            'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,' + \
            '*/*;q=0.8',
            'Accept-Language: en-US,en;q=0.5',
            'Cache-Control: max-age=0',
            'Connection: keep-alive',
            'DNT: 1',
         ]

url = 'http://www.reddit.com/'

spider = pycurl.Curl()
buf = cStringIO.StringIO()

spider.setopt(spider.WRITEFUNCTION, buf.write)
spider.setopt(spider.URL, url)
spider.setopt(spider.HTTPHEADER, HEADER)

spider.perform()
html = fromstring(buf.getvalue())
data = []
links = html.cssselect("div.sitetable a.title")
for link in links:
    info = {}
    info['text'] = link.text
    info['link'] = link.get('href')
    data.append(info)

pprint.pprint(data) 

prepositions = ['at', 'to', 'for', 'of', 'about', 'after', 'before', 'in', 'from', 'with'] 
def link_jack(links):
    new_links = []
    for link in links:
        for word in link['text'].split():
            new_title = link['text']
            if word in prepositions:
                # pdb.set_trace()
                new_title = link['text'][:link['text'].index(word) + len(word)] + "..."
                break
        new_links.append({'text':new_title, 'link':link['link']})
    return new_links

pprint.pprint(link_jack(data))
        


