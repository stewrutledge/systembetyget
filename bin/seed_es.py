#!/usr/bin/env python

import xml.etree.ElementTree as ET
import urllib2
from pyelasticsearch import ElasticSearch

es = ElasticSearch('http://localhost:9200/')

# This is for downloading directly from systembolaget
response = urllib2.urlopen(
    'http://www.systembolaget.se/Assortment.aspx?Format=Xml')
tree = ET.parse(response)
# For local use (so systembolaget doesn't get annoyed
#tree = ET.parse('articles.xml')
root = tree.getroot()
articles = {}
list = []


def isint(string):
    try:
        int(string)
        return True
    except ValueError:
        return False


def isflt(string):
    try:
        float(string)
        return True
    except ValueError:
        return False


for item in root.findall('artikel'):
    list.append(articles)
    articles = {}
    for subitem in item:
        if subitem.text is not None:
            if isint(subitem.text):
                articles[subitem.tag] = int(subitem.text)
            elif isflt(subitem.text):
                articles[subitem.tag] = float(subitem.text)
            else:
                articles[subitem.tag] = subitem.text


for i, article in enumerate(list):
    if len(article) == 0:
        print "Empty value found"
    else:
        print es.index('articles3', 'article', article, id=i)
