import pycurl
import nltk
import cStringIO
import pprint
from lxml.html import fromstring
import pdb

header = [
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
def crawl(url, header):
    spider = pycurl.Curl()
    buf = cStringIO.StringIO()

    spider.setopt(spider.WRITEFUNCTION, buf.write)
    spider.setopt(spider.URL, url)
    spider.setopt(spider.HTTPHEADER, header)

    spider.perform()
    html = buf.getvalue()
    return html

def mine_reddit(raw):
    html = fromstring(raw)
    data = []
    links = html.cssselect("div.sitetable a.title")
    for link in links:
        info = {}
        info['text'] = link.text
        info['link'] = link.get('href')
        data.append(info)
    return data

def bait_text(text, pos):
    tags = nltk.pos_tag(nltk.word_tokenize(text))
    new_text = text + "..."        
    for word in tags:
        if word[1] == pos.upper():
            cut_on = text.index(word[0])
            new_text = text[:cut_on + len(word[0])] + "..."
    return new_text 

def jack_link(link, pos):
    new_text = bait_text(link['text'], pos) 
    return {'link': link['link'], 'text': new_text}

def jack_links(links, pos):
    new_links = []
    for link in links:
        new_links.append(jack_link(link, pos))
    return new_links

if __name__ == "__main__":
    html = crawl(url, header) 
    data = mine_reddit(html)
    pprint.pprint(data) 
    pprint.pprint(jack_links(data, "in"))
