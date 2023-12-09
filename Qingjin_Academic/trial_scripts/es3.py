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
    search_term = "Nancy"
    author_filter = "作者A"
    journal_filter = "期刊B"

    # 构建查询体
    search_body = {
        "query": {
            # "match": {
            #     "*": search_term
            # }
            "query_string": {
                "query": search_term
            }
        },
        "size": 20,  # 指定每页返回的结果数量
        "from": 0,  # 指定从搜索结果中的第几条开始返回，用于分页
        # "sort": [
        #     {"": {"order": "desc"}}  # 指定排序字段和排序顺序
        # ],
        "aggs": {
            # "author_all": {  # 聚合作者信息
            #     "terms": {
            #         "field": "author_all.keyword"
            #     }
            # },
            # "author_all": {  # 聚合作者信息
            #     "terms": {
            #         "script": {
            #             "source": """
            #                 def authorsField = doc["author_all.keyword"];
            #                       if (authorsField != null && !authorsField.empty) {
            #                           def authors = authorsField.value.splitOnToken('|');
            #                           def processedAuthors = [];
            #                           for (author in authors) {
            #                               def trimmedAuthor = author.trim();
            #                               if (!trimmedAuthor.isEmpty()) {
            #                                   processedAuthors.add(trimmedAuthor);
            #                               }
            #                           }
            #                           return processedAuthors;
            #                       }
            #                       return [];
            #             """,
            #             "lang": "painless"
            #         }
            #     }
            # },
            # "author_main": {  # 聚合主要作者信息
            #     "terms": {
            #         "field": "author_main.keyword"
            #     }
            # },
            "display_name": {  # 聚合作者信息
                "terms": {"field": "display_name.keyword"}
            },
            "institution": {
                "terms": {"field": "institution.keyword"}  # 聚合机构信息
            },
            "domain": {  # 聚合作者信息
            "terms": {
                "script": {
                    "source": """
                            def domainsField = doc["domain.keyword"];
                                  if (domainsField != null && !domainsField.empty) {
                                      def domains = domainsField.value.splitOnToken('|');
                                      def processedDomains = [];
                                      for (domain in domains) {
                                          def trimmedDomain = domain.trim();
                                          if (!trimmedDomain.isEmpty()) {
                                              processedDomains.add(trimmedDomain);
                                          }
                                      }
                                      return processedDomains;
                                  }
                                  return [];
                        """,
                    "lang": "painless"
                }
            }
        }
        }
        # "post_filter": {
        #     "bool": {
        #         "must": [
        #             {"term": {"author.keyword": author_filter}},  # 筛选作者
        #             {"term": {"journal.keyword": journal_filter}}  # 筛选期刊
        #         ]
        #     }
        # }
    }
    time = datetime.datetime.now()
    # 执行搜索
    result = esConnection.search(index="authors", body=search_body)

    # 处理搜索结果
    for hit in result['hits']['hits']:
        print(hit['_source'])
    print(len(result['hits']['hits']))
    display_name_agg = result['aggregations']['display_name']['buckets']
    institution_agg = result['aggregations']['institution']['buckets']

    print("Display Name Aggregation:")
    for key in result['aggregations']['display_name']:
        print(key, result['aggregations']['display_name'][key])
    for bucket in display_name_agg:
        print(bucket['key'], bucket['doc_count'])
    print("Institution Aggregation:")
    for key in result['aggregations']['institution']:
        print(key, result['aggregations']['institution'][key])
    for bucket in institution_agg:
        print(bucket['key'], bucket['doc_count'])

    print(datetime.datetime.now() - time)

    # search_body = {
    # }
    # result = esConnection.search(index="works", body=search_body)
    # print(type(result), result)
    # print(len(result['hits']['hits']))
    # for hit in result['hits']['hits']:
    #     print(type(hit), hit)
    #     hit0 = hit['_source']
    #     print(type(hit0), hit0)
    #     for key in hit0.keys():
    #         print(key, hit0[key])
    #     break
