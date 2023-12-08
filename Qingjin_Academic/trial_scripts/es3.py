import datetime
import json
import requests
from elasticsearch_dsl import Search, connections
from elasticsearch_dsl.query import MultiMatch, Match

if __name__ == '__main__':
    requests.packages.urllib3.disable_warnings()
    config = json.load(open('./../config.json', 'r'))
    print(config["elasticsearch_HOST"])
    elasticsearch_HOSTS = [config["elasticsearch_HOST"]]
    esConnection = connections.create_connection(hosts=elasticsearch_HOSTS,
                                                 http_auth=(config["elasticsearch_USER"],
                                                            config["elasticsearch_PASSWORD"]),
                                                 verify_certs=False)
    search_term = "AI"
    author_filter = "作者A"
    journal_filter = "期刊B"

    # 构建查询体
    search_body = {

    }

    # 执行搜索
    result = esConnection.search(index="works", body=search_body)

