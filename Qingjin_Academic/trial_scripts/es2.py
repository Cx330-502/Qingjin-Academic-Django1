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
    search_term = "Computer Science"
    author_filter = "作者A"
    journal_filter = "期刊B"

    # 构建查询体
    search_body = {
        "query": {
            # "match": {
            #     "*": search_term
            # }
            "query_string": {
                "query": search_term,
                "fields": ["*"]
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
            # "source": {
            #     "terms": {"field": "source.keyword"}  # 聚合期刊信息
            # },
            # "publication_date": {
            #     "date_histogram": {
            #         "field": "publication_date",
            #         # "fixed_interval": "1y"  # 按年聚合
            #         "calendar_interval": "1y"  # 按年聚合
            #     }
            # },
            # "domain": {
            #     "terms": {"field": "domain_main.keyword"}  # 聚合领域信息
            # }
        },
        "highlight": {
            "fields": {
                "*": {}  # 指定要高亮的字段为 "content"
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
    print(time.strftime("YYYY-MM-DD HH:MM:SS"))
    # 执行搜索
    result = esConnection.search(index="concepts", body=search_body)

    # 处理搜索结果
    # 处理搜索结果和高亮
    for hit in result['hits']['hits']:
        source = hit['_source']
        highlight = hit.get('highlight', {})

        # 打印原始结果和高亮文本
        print("Original Source:", source)
        print("Highlight:", highlight)
        print(type(highlight))
        print("----------------------")
    print(len(result['hits']['hits']))
    # authors_aggregation = result['aggregations']['author_main']['buckets']
    # source_aggregation = result['aggregations']['source']['buckets']
    # publication_date_aggregation = result['aggregations']['publication_date']['buckets']
    # domain_aggregation = result['aggregations']['domain']['buckets']
    # print("Authors:")
    # print(len(authors_aggregation))
    # for key in result['aggregations']['author_main'].keys():
    #     print(key, result['aggregations']['author_main'][key])
    # z = 0
    # for author_bucket in authors_aggregation:
    #     print(f"{author_bucket['key']}: {author_bucket['doc_count']}")
    #     z += author_bucket['doc_count']
    # print(z)

    # print("Source:")
    # print(len(source_aggregation))
    # z = 0
    # for source_bucket in source_aggregation:
    #     print(f"{source_bucket['key']}: {source_bucket['doc_count']}")
    #     z += source_bucket['doc_count']
    # print(z)
    #
    # print("Publication Date:")
    # print(len(publication_date_aggregation))
    # for key in result['aggregations']['publication_date']:
    #     print(key, result['aggregations']['publication_date'][key])
    # z = 0
    # for publication_date_bucket in publication_date_aggregation:
    #     print(f"{publication_date_bucket['key_as_string']}: {publication_date_bucket['doc_count']}")
    #     z += publication_date_bucket['doc_count']
    # print(z)
    #
    # print("Domain:")
    # print(len(domain_aggregation))
    # z = 0
    # for domain_bucket in domain_aggregation:
    #     print(f"{domain_bucket['key']}: {domain_bucket['doc_count']}")
    #     z += domain_bucket['doc_count']
    # print(z)

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
