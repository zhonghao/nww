from babylon import backends
from babylon import qs
from babylon import topics
import json


def test_save_article():
    article = {
        "id": "544cc5e6970a310a7f613fbc",
        "type": "article",
        "date": "2014-10-09T07:57:35.879Z",
        "quotes": [
            {
            "person": {
              "handle": "angela-merkel",
              "name": "Angel Merkel",
              "position": "Chancellor of the Federal Republic of Germany"
            },
            "source_id": "544cc4e1970a310984e9f276",
            "source_url": "http://www.spiegel.de/politik/ausland/wahl-in-der-ukraine-poroschenko-laut-umfragen-favorit-a-971259.html",
            "text": "Die zerr\u00fcttete Ukraine w\u00e4hlt am Sonntag einen neuen Pr\u00e4sidenten. Milliard\u00e4r Poroschenko hat beste Chancen. Doch was ist mit Gasprinzessin Tymoschenko? Und wie verh\u00e4lt sich Russland? Antworten auf die wichtigsten Fragen vor der Wahl.",
            "topics": [],
            "type": "quote"
          }
        ],
        "people": [
            {
                "handle": "angela-merkel",
                "name": "Angel Merkel"
            }
        ],
        "topics": [
            {
                "handle": "mh-17-crash"
            }
        ],
        "tags": [
            {
                "handle": "mh-17-crash"
            }
        ]
    }

    article2 = {
        "id": "544cc5e6970a310a7f614fbc",
        "type": "article",
        "date": "2014-10-09T07:57:35.879Z",
        "quotes": [
        ],
        "people": [
            {
                "handle": "putin",
            }
        ],
        "topics": [
            {
                "handle": "mh-17-crash"
            }
        ],
        "tags": [
            {
                "handle": "war"
            }
        ]
    }

    assert backends.articles.count() == 0
    assert backends.quote_collections.count() == 0

    backends.save_content(article)
    backends.save_content(article2)

    assert backends.articles.count() == 2
    assert backends.quote_collections.count() == 1

    quote = backends.quote_collections.find_one()
    assert quote['topics'][0]['handle'] == 'mh-17-crash'


    results = backends.find()
    assert len(results) == 3

    results = backends.find(people=['putin'])
    assert len(results) == 1

    results = backends.find(people=['angela-merkel'])
    assert len(results) == 2



# def test_save():
#     json_obj = """{
#       "description": "",
#       "id": "544bc580970a31081f7ede92",
#       "meta": {
#         "people": [
#           {
#             "handle": "vladimir-putin",
#             "img_url": "http://localhost:5050/img/person/vladimir-putin/icon",
#             "name": "Vladimir Putin",
#             "position": "President of Russian Federation"
#           },
#           {
#             "handle": "angela-merkel",
#             "img_url": "http://localhost:5050/img/person/angela-merkel/icon",
#             "name": "Angela Merkel",
#             "position": "Chancellor of the Federal Republic of Germany"
#           }
#         ],
#         "tags": [
#           {
#             "handle": "global-energy",
#             "name": "Global Energy"
#           },
#           {
#             "handle": "economy",
#             "name": "Economy"
#           }
#         ],
#         "topics": [
#           {
#             "handle": "mh-17-crash",
#             "img_url": "http://localhost:5050/img/topic/mh-17-crash/icon",
#             "name": "MH 17 Crash"
#           }
#         ]
#       },
#       "og": {
#         "description": "Twitter\u2019s engineering group, known for various contributions to open source from streaming MapReduce to front-end framework Bootstrap recently announced open sourcing an algorithm that can efficiently recommend content. LinkedIn also open sourced a Machine Learning library of its own, ml-ease.  In this article we present the algorithms and what they mean for the open source community.",
#         "image": "http://cdn3.infoq.com/styles/i/logo-big.jpg",
#         "site_name": "InfoQ",
#         "title": "LinkedIn and Twitter Contribute Machine Learning Libraries to Open Source ",
#         "type": "website"
#       },
#       "people": [
#         {
#           "handle": "angela-merkel",
#           "img_url": "http://sleepy-mountain-8434.herokuapp.com/img/person/angela-merkel/icon",
#           "name": "Angela Merkel",
#           "position": "Chancellor of the Federal Republic of Germany"
#         }
#       ],
#       "quotes": [
#         {
#           "person_handle": "angela-merkel",
#           "person_name": "Angela Merkel",
#           "source_id": "544bc580970a31081f7ede92",
#           "source_url": "http://www.infoq.com/news/2014/10/LinkedIn-Twitter-ML-Open-Source",
#           "text": "this is a quote"
#         }
#       ],
#       "rating": 2,
#       "source_url": "http://www.infoq.com/news/2014/10/LinkedIn-Twitter-ML-Open-Source",
#       "tags": [
#         {
#           "handle": "economy",
#           "name": "Economy"
#         }
#       ],
#       "time": "",
#       "title": "",
#       "topics": [
#         {
#           "handle": "mh-17-crash",
#           "img_url": "http://sleepy-mountain-8434.herokuapp.com/img/topic/mh-17-crash/icon",
#           "name": "MH 17 Crash"
#         }
#       ],
#       "type": "article"
#     }"""
#     backends.store_article(json.loads(json_obj))
#     backends.save_content(json.loads(json_obj))
#     res = backends.query(people=['angela-merkel'])
#     assert backends.articles.find().count() == 1
#     assert backends.articles.find({'people.handle': 'angela-merkel'}).count() == 1
#     assert len(res['articles']) == 1
#     assert len(res['quotes']) == 1
    

# # def test_query():
# #     url = 'fun'
# #     a = backends.get_article(url)
# #     # url2 = 'fun2'
# #     backends.store_article(a)
# #     # assert backends.article.find().count() == 1
# #     counter = 0 
# #     for a in backends.query('source_url', 'fun', backends.articles):
# #         counter += 1
# #         assert a['source_url'] == 'fun'
# #    assert counter == 1
    

# def test_article_get_or_create():
#     url = 'fun'
#     a = backends.get_article(url)
#     assert a['title'] == ''
#     assert a['source_url'] == url


# # def test_quote():
# #     # insert quote
# #     backends.store_quote('hi', '110', 'http://cliqz.com/', '123', 'Thomas', 'T')
# #     # retrieve quote
# #     for q in backends.get_quote(person_id='T'):
# #         assert q['type'] == "quote"


# def test_topics():
#     backends.store_topic('title', '', {'a': 'b'})
#     for t in backends.get_topic(title='title'):
#         assert t['entity_type'] == 'topic'


# def test_store_article():
#     url = 'fun'
#     assert backends.articles.find({'url': url}).count() == 0
#     a = backends.get_article(url)
#     backends.store_article(a)
#     a = backends.get_article(url)
#     assert a['source_url'] == 'fun'


# def test_person_get_or_create():
#     handle = 'h'
#     assert backends.persons.find({'handle': handle}).count() == 0
#     p = backends.get_person(handle)
#     assert p['handle'] == handle
#     assert 'meta' in p


# def test_link():
#     a = backends.get_article('a')
#     t = backends.get_tag('t')
#     backends.link(backends.articles, a['id'], 'tags', t['id'])
#     a = backends.get_article('a')
#     assert a['tags'] == [t['id']]


def setup_module(module):
    backends.redis_conn.flushall()
    backends.mongo_conn.drop_database(backends.MONGO_DB_NAME)
