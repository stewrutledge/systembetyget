#!/usr/bin/env python

import xml.etree.ElementTree as ET
import urllib2
from pyelasticsearch import ElasticSearch

es = ElasticSearch('http://localhost:9200/')

response = urllib2.urlopen('http://www.systembolaget.se/Assortment.aspx?Format=Xml')
tree = ET.parse(response)
root = tree.getroot()
articles = {}
list = []

for item in root.findall('artikel'):
    list.append(articles)
    articles = {}
    for subitem in item:
        articles[subitem.tag] = subitem.text

for i,article in enumerate(list):
    if len(article) == 0:
        print "Empty value found"
    else:
        print es.index('articles','article',article,id=i)
