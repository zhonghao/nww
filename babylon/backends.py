import datetime
import os
import pymongo
import redis
import urlparse
from bson.objectid import ObjectId

import article
import meta
import person
import qs
import tag
import topics


redis_url = os.environ['REDISCLOUD_URL']
redis_url = urlparse.urlparse(redis_url)
redis_conn = redis.Redis(
    host=redis_url.hostname,
    port=redis_url.port,
    password=redis_url.password)

mongo_url = os.environ['MONGOHQ_URL']
mongo_conn = pymongo.MongoClient(mongo_url)


MONGO_DB_NAME = 'babylon'

ARTICLES_COLLECTION = 'articles'
PERSONS_COLLECTION = 'persons'
TAGS_COLLECTION = 'tags'

db = mongo_conn[MONGO_DB_NAME]
articles = db[ARTICLES_COLLECTION]
persons = db[PERSONS_COLLECTION]
tags = db[TAGS_COLLECTION]

def time():
    return datetime.datetime.utcnow().isoformat()

def link(collection, id1, relation, id2):
    oid1 = ObjectId(id1)
    collection.update({'_id': oid1}, {'$addToSet': {relation: id2}})

def get_article(url):
    return get_or_create(articles, {"source_url": url}, article.template)

def store_article(article):
    articles.save(with_mongo_id(article))


def get_person(handle):
    return get_or_create(persons, {"handle": handle}, person.template)

def store_person(person):
    persons.save(with_mongo_id(person))


def get_tag(name):
    return get_or_create(tags, {"name": name}, tag.template)

def store_tag(tag):
    tags.save(with_mongo_id(tag))


def with_mongo_id(obj):
    obj['_id'] = ObjectId(obj['id'])
    return obj

def get_or_create(collection, spec, template):
    a = collection.find_one(spec)
    if not a:
        assert len(spec.values()) == 1
        a = template(spec.values()[0])
        oid = ObjectId()
        a['_id'] = oid
        a['id'] = unicode(oid)
        collection.save(a)
    return json_ready(a)

def json_ready(article):
    article.update(dict(id=unicode(article['_id']), meta=get_meta()))
    article.pop('_id')
    return article

def get_meta():
    return meta.get_meta()

    
QUOTES_COLLECTION = 'quotes'
TOPICS_COLLECTION = 'topics'

db = mongo_conn[MONGO_DB_NAME]

articles = db[ARTICLES_COLLECTION]
quote_collections = db[QUOTES_COLLECTION]
topic_collections = db[TOPICS_COLLECTION]


# quotes
def get_quote(_id=None, person_id=None, source_id=None):
    if _id:
        query = {'_id': _id}
    if person_id:
        query = {'person_id': person_id}
    if source_id:
        query = {'source_id': source_id}
    for q in quote_collections.find(query):
            yield q


def store_quote(quote_content, time, source_url, person_name,
                source_id=None, person_id=None, topics=[], tags=[]):
    content = qs.template(
        quote_content, time, source_url, person_name,
        source_id, person_id, topics, tags)
    return quote_collections.insert(content)


# topics
def store_topic(title, desc='', url='', people='', translation={}, editors={}):
    # if topic exist, update
    if topic_collections.find({'title': title}):
        return topic_collections.update(
            {'title': title},
            {'$addToSet': {"url": url, "people": people}})
    else:
        content = topics.template(title, desc, url, people, translation, editors)
        return topic_collections.insert(content)


def get_topic(_id=None, title=None):
    if _id:
        query = {'_id': _id}
    if title:
        query = {'title': title}
    for q in topic_collections.find(query):
            yield q
