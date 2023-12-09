import json
import requests
from elasticsearch_dsl import Search, connections
from elasticsearch_dsl.query import MultiMatch, Match

esConnection = None


def es_connect():
    global esConnection
    if esConnection is None or not esConnection.ping():
        requests.packages.urllib3.disable_warnings()
        config = json.load(open('config.json', 'r', encoding='utf-8'))
        es_co = connections.create_connection(hosts=[config["elasticsearch_HOST"]],
                                              http_auth=(config["elasticsearch_USER"],
                                                         config["elasticsearch_PASSWORD"]),
                                              verify_certs=False)
        esConnection = es_co
    else:
        return


def body_search(index, body, timeout):
    es_connect()
    result = esConnection.search(index=index, body=body, timeout=12000)
    return result


def search_query(search, query):
    es_connect()
    s = search.query(query)
    response = s.execute()
    for hit in response.hits:
        print(type(hit))
        print(hit)
        print(hit.to_dict())
        temp = hit.to_dict()
        for key in temp.keys():
            print(key, temp[key])
        break
