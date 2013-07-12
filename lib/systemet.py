#!/usr/bin/env python

from pyelasticsearch import ElasticSearch
from pymongo import MongoClient
import numpy
from math import ceil

es = ElasticSearch('http://localhost:9200/')
mongo_client = MongoClient()
db = mongo_client.test2

class AutoVivification(dict):
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value

def query(search_string,
          limit=None,target=None, from_value=None, to_value=None):
    query = AutoVivification()
    query['query']['filtered']['query']['query_string']['query'] = search_string
    if target and from_value and to_value:
        query['query']['filtered']['filter']['range'][str(target)]['from'] = round(from_value,2)
        query['query']['filtered']['filter']['range'][str(target)]['to'] = round(to_value,2)
    print query
    result = es.search(query, index='articles3', size=limit)
    return result


def fetch_rating(articleid=None):
    post = db.posts.find_one({"name": articleid})
    rating = post['current_rating']
    return rating


def add_rating(articleid=None, rating=None):
    post = db.posts.find_one({"name": articleid})
    db.posts.update({"name": articleid}, {"$push": {"ratings": int(rating)}})
    db.posts.update({"name": articleid}, {"$set": {"current_rating": round(numpy.mean(post.get("ratings")),2)}})
