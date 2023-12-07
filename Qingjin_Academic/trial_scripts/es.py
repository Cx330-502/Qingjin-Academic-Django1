import json
import requests
from elasticsearch_dsl import Search, connections
from elasticsearch_dsl.query import MultiMatch, Match


def search_query(search, query):
    s = search.query(query)
    response = s.execute()
    print(response.hits.total)
    i = 0
    for hit in response.hits:
        print(type(hit))
        print(hit)
        print(hit.to_dict())
        temp = hit.to_dict()
        for key in temp.keys():
            print(key, temp[key])
        break


if __name__ == '__main__':
    requests.packages.urllib3.disable_warnings()
    config = json.load(open('./../config.json', 'r'))
    print(config["elasticsearch_HOST"])
    elasticsearch_HOSTS = [config["elasticsearch_HOST"]]
    esConnection = connections.create_connection(hosts=elasticsearch_HOSTS,
                                                 http_auth=(config["elasticsearch_USER"],
                                                            config["elasticsearch_PASSWORD"]),
                                                 verify_certs=False)
    # search = Search(index='institutions')
    # query = Match(display_name='Vision')
    # search_query(search, query)
    # search_body = {
    #     "query": {
    #         "match_all": {}  # 可以根据需要修改查询条件
    #     },
    #     "sort": [
    #         {"cited_count": {"order": "desc"}}  # 根据引用量字段降序排序
    #     ],
    #     # sort后的结果对应的是sort,真实结果在_source字段下
    #     "size": 10  # 获取前十条结果
    # }
    # result = esConnection.search(index="works", body=search_body)
    # print(type(result), result)
    # for hit in result['hits']['hits']:
    #     print(type(hit), hit)
    #     hit0 = hit['_source']
    #     print(type(hit0), hit0)
    #     # for key in hit0.keys():
    #     #     print(key, hit0[key])
    #     # break
    result_ids = [2330584152, 16253337]
    search_body = {
        "query": {
            "terms": {
                "_id": result_ids
            }
        }
    }
    result = esConnection.search(index="works", body=search_body)
    print(type(result), result)
    print(len(result['hits']['hits']))
    for hit in result['hits']['hits']:
        print(type(hit), hit)
        hit0 = hit['_source']
        print(type(hit0), hit0)
        for key in hit0.keys():
            print(key, hit0[key])
        break
