import re
from datetime import datetime
import ES_scripts.es_search_script as es_search
from Academic_models.models import Star, Scholar, Paper_delete


def author_all_field_handle(author_all):
    if author_all == '' or author_all is None:
        return []
    author_list = []
    authors = author_all.split('|')
    for author_info in authors:
        if author_info == '':
            continue
        author_info = author_info.strip()
        # 按照 "&" 分割不同字段
        author_fields = [field.strip() for field in author_info.split('&') if field.strip()]
        if len(author_fields) < 2:
            continue
        # 将字段组成字典
        author_dict = {
            "name": author_fields[0].strip(),  # 第一个字段为姓名
            "id": author_fields[1].strip()  # 第二个字段为ID（假设有两个字段）
        }
        if Scholar.objects.filter(es_id=author_fields[1], claimed_user_id__isnull=False).exists():
            author_dict['claimed'] = True
        else:
            author_dict['claimed'] = False

        # 将每个作者的信息添加到列表中
        author_list.append(author_dict)
    return author_list


def domain_field_handle(domain):
    if domain == '' or domain is None:
        return []
    domain_list = []
    domains = domain.split('|')
    for domain_info in domains:
        if domain_info == '':
            continue
        domain_info = domain_info.strip()
        # 按照 "&" 分割不同字段
        domain_fields = [field.strip() for field in domain_info.split('&') if field.strip()]
        if len(domain_fields) < 4:
            continue
        # 将字段组成字典
        domain_dict = {
            "name": domain_fields[0],  # 第一个字段为姓名
            "id": domain_fields[1],  # 第二个字段为ID（假设有两个字段）
            "level": domain_fields[2],
            "activity_level": domain_fields[3]
        }
        # 将每个作者的信息添加到列表中
        domain_list.append(domain_dict)
    return domain_list


def institution_field_handle(institution):
    if institution == '' or institution is None:
        return []
    institution_list = []
    institutions = institution.split('|')
    for institution_info in institutions:
        if institution_info == '':
            continue
        institution_info = institution_info.strip()
        # 按照 "&" 分割不同字段
        institution_fields = [field.strip() for field in institution_info.split('&') if field.strip()]
        if len(institution_fields) < 2:
            continue
        # 将字段组成字典
        institution_dict = {
            "name": institution_fields[0],  # 第一个字段为姓名
            "id": institution_fields[1],  # 第二个字段为ID（假设有两个字段）
        }
        # 将每个作者的信息添加到列表中
        institution_list.append(institution_dict)
    return institution_list


def source_field_handle(source):
    if source == '' or source is None:
        return []
    source_list = []
    sources = source.split('|')
    for source_info in sources:
        if source_info == '':
            continue
        source_info = source_info.strip()
        # 按照 "&" 分割不同字段
        source_fields = [field.strip() for field in source_info.split('&') if field.strip()]
        if len(source_fields) < 3:
            continue
        # 将字段组成字典
        source_dict = {
            "name": source_fields[0],  # 第一个字段为姓名
            "type": source_fields[1],  # 第二个字段为type（假设有两个字段）
            "id": source_fields[2]
        }
        # 将每个作者的信息添加到列表中
        source_list.append(source_dict)
    return source_list


def hot_paper_handle(result):
    result_data = []
    for hit0 in result['hits']['hits']:
        try:
            for key in hit0['highlight']:
                hit0['_source'][key] = hit0['highlight'][key][0]
        except:
            pass
        hit = {}
        hit['title'] = hit0['_source']['title']
        hit['id'] = hit0['_source']['id']
        hit['cited_count'] = hit0['_source']['cited_count']
        hit['author_all'] = author_all_field_handle(hit0['_source'].get('author_all', ""))
        hit['publication_date'] = hit0['_source']['publication_date']
        result_data.append(hit)
    return result_data


def hot_institution_handle(result):
    result_data = []
    for hit0 in result['hits']['hits']:
        try:
            for key in hit0['highlight']:
                hit0['_source'][key] = hit0['highlight'][key][0]
        except:
            pass
        hit = {}
        hit['display_name'] = hit0['_source']['display_name']
        hit['id'] = hit0['_source']['id']
        hit['image_url'] = hit0['_source'].get('image_url', "")
        hit['ror'] = hit0['_source']['ror']
        hit['summary_stats'] = handle_summary_stats(hit0['_source']['summary_stats'])
        result_data.append(hit)
    return result_data


def author_handle(result_1):
    result_data = []
    for hit0 in result_1['hits']['hits']:
        try:
            for key in hit0['highlight']:
                hit0['_source'][key] = hit0['highlight'][key][0]
        except:
            pass
        hit = {}
        hit['display_name'] = hit0['_source']['display_name']
        hit['id'] = hit0['_source']['id']
        hit['most_cited_work'] = hit0['_source'].get('most_cited_work', "")
        hit['cited_by_count'] = hit0['_source']['cited_by_count']
        hit['summary_stats'] = handle_summary_stats(hit0['_source']['summary_stats'])
        hit['orcid'] = hit0['_source'].get('orcid', "")
        if Scholar.objects.filter(es_id=hit['id'], claimed_user_id__isnull=False).exists():
            hit['claimed'] = True
        else:
            hit['claimed'] = False
        result_data.append(hit)
    return result_data


def concept_handle(result_3):
    result_data = []
    for hit0 in result_3['hits']['hits']:
        try:
            for key in hit0['highlight']:
                hit0['_source'][key] = hit0['highlight'][key][0]
        except:
            pass
        hit = {}
        hit['display_name'] = hit0['_source']['display_name']
        hit['id'] = hit0['_source']['id']
        hit['description'] = hit0['_source'].get('description', "")
        hit['summary_stats'] = handle_summary_stats(hit0['_source']['summary_stats'])
        hit['level'] = hit0['_source']['level']
        hit['image_url'] = hit0['_source'].get('image_url', "")
        result_data.append(hit)
    return result_data


def cancel_highlight(result):
    result = str(result)
    result = processed_string = re.sub(r'<em>.*?</em>', '', result)
    return result


def paper_handle2(result):
    result_data = []
    for hit0 in result['hits']['hits']:
        try:
            for key in hit0['highlight']:
                hit0['_source'][key] = hit0['highlight'][key][0]
        except:
            pass
        hit = {}
        hit['title'] = hit0['_source']['title']
        hit['id'] = cancel_highlight(hit0['_source']['id'])
        hit['abstract'] = hit0['_source'].get('abstract', "")
        hit['cited_count'] = hit0['_source']['cited_count']
        hit['domain'] = domain_field_handle(hit0['_source']['domain'])
        hit['author_all'] = author_all_field_handle(hit0['_source'].get('author_all', ""))
        hit['pdf_url'] = hit0['_source'].get('pdf_url', "")
        hit['landing_page_url'] = hit0['_source'].get('landing_page_url', "")
        hit['source'] = source_field_handle(hit0['_source'].get('source', ""))
        hit['publication_date'] = hit0['_source']['publication_date']
        hit['type_num'] = hit0['_source']['type_num']
        result_data.append(hit)
    return result_data


def institution_handle2(result):
    result_data = []
    for hit0 in result['hits']['hits']:
        try:
            for key in hit0['highlight']:
                hit0['_source'][key] = hit0['highlight'][key][0]
        except:
            pass
        hit = {}
        hit['display_name'] = hit0['_source']['display_name']
        hit['display_name_acronyms'] = hit0['_source'].get('display_name_acronyms', "")
        hit['country_code'] = hit0['_source'].get('country_code', "")
        hit['image_url'] = hit0['_source'].get('image_url', "")
        hit['id'] = cancel_highlight(hit0['_source']['id'])
        hit['summary_stats'] = handle_summary_stats(hit0['_source']['summary_stats'])
        hit['homepage_url'] = hit0['_source'].get('homepage_url', "")
        hit['type'] = hit0['_source'].get('type', "")
        hit['domain'] = domain_field_handle(hit0['_source']['domain'])
        hit['geo'] = hit0['_source'].get('geo', "")
        hit['ror'] = hit0['_source'].get('ror', "")
        result_data.append(hit)
    return result_data


def author_handle2(result_1):
    result_data = []
    for hit0 in result_1['hits']['hits']:
        try:
            for key in hit0['highlight']:
                hit0['_source'][key] = hit0['highlight'][key][0]
        except:
            pass
        hit = {}
        hit['display_name'] = hit0['_source']['display_name']
        hit['domain'] = domain_field_handle(hit0['_source']['domain'])
        hit['institution'] = institution_field_handle(hit0['_source'].get('institution', ""))
        hit['most_cited_work'] = hit0['_source'].get('most_cited_work', "")
        hit['cited_by_count'] = hit0['_source']['cited_by_count']
        hit['summary_stats'] = handle_summary_stats(hit0['_source']['summary_stats'])
        hit['id'] = cancel_highlight(hit0['_source']['id'])
        hit['orcid'] = hit0['_source'].get('orcid', "")
        if Scholar.objects.filter(es_id=hit['id'], claimed_user_id__isnull=False).exists():
            hit['claimed'] = True
        else:
            hit['claimed'] = False
        result_data.append(hit)
    return result_data


def concept_handle2(result_3):
    result_data = []
    result_data = []
    for hit0 in result_3['hits']['hits']:
        try:
            for key in hit0['highlight']:
                hit0['_source'][key] = hit0['highlight'][key][0]
        except:
            pass
        hit = {}
        hit['display_name'] = hit0['_source']['display_name']
        hit['description'] = hit0['_source'].get('description', "")
        hit['id'] = cancel_highlight(hit0['_source']['id'])
        hit['summary_stats'] = handle_summary_stats(hit0['_source']['summary_stats'])
        hit['level'] = hit0['_source']['level']
        hit['image_url'] = hit0['_source'].get('image_url', "")
        hit['ancestors'] = hit0['_source'].get('ancestors', "")
        result_data.append(hit)
    return result_data


search_type_table = ['works', 'authors', 'institutions', 'concepts']
com_table = [{
    'Title': 'title',
    'Abstract': 'abstract',
    'Domain': 'domain',
    'Author': 'author_all',
    'Source': 'source',
    'Main Author': 'author_main',
    'Main Domain': 'domain_main',
    'ID': 'id',
    'Referenced Works': 'referenced_works',
    'corresponding_institution_ids': 'corresponding_institution_ids'
}, {
    'Name': 'display_name',
    'Domain': 'domain',
    'Institution': 'institution',
    'Most Representative Work': 'most_cited_work',
    'Orcid': 'orcid',
    'ID': 'id',
}, {
    'Name': 'display_name',
    'Acronyms': 'display_name_acronyms',
    'Country Code': 'country_code',
    'Institution Type': 'institution_type',
    'Domain': 'domain',
    'Main Domain': 'domain_main',
    'Ror': 'ror',
    'ID': 'id',
}, {
    'Name': 'display_name',
    'Description': 'description',
    'Concept Level': 'level',
    'ID': 'id',
}
]


def handle_search_list_1(search_type, and_list, or_list, not_list, start_time, end_time):
    must_list = []
    should_list = []
    must_not_list = []
    highlight = {"fields": {}}
    if len(and_list) + len(or_list) + len(not_list) == 1 and and_list[0]['select'] == "":
        if search_type == 0:
            should_list.append({"match": {
                "title": {
                    "query": and_list[0]['content'],
                    "minimum_should_match": "75%"
                }}})
            should_list.append({"match": {
                "abstract": {
                    "query": and_list[0]['content'],
                    "minimum_should_match": "75%"
                }}})
            should_list.append({"match": {
                "domain": {
                    "query": and_list[0]['content'],
                    "minimum_should_match": "75%"
                }}})
            should_list.append({"match": {
                "author_all": {
                    "query": and_list[0]['content'],
                    "minimum_should_match": "75%"
                }}})
            should_list.append({"match": {
                "source": {
                    "query": and_list[0]['content'],
                    "minimum_should_match": "75%"
                }}})
            highlight['fields']['title'] = {}
            highlight['fields']['abstract'] = {}
            highlight['fields']['domain'] = {}
            highlight['fields']['author_all'] = {}
            highlight['fields']['source'] = {}
        elif search_type == 1:
            should_list.append({"match": {
                "display_name": {
                    "query": and_list[0]['content'],
                    "minimum_should_match": "75%"
                }}})
            should_list.append({"match": {
                "domain": {
                    "query": and_list[0]['content'],
                    "minimum_should_match": "75%"
                }}})
            should_list.append({"match": {
                "institution": {
                    "query": and_list[0]['content'],
                    "minimum_should_match": "75%"
                }}})
            should_list.append({"match": {
                "most_cited_work": {
                    "query": and_list[0]['content'],
                    "minimum_should_match": "75%"
                }}})
            highlight['fields']['display_name'] = {}
            highlight['fields']['domain'] = {}
            highlight['fields']['institution'] = {}
            highlight['fields']['most_cited_work'] = {}
        elif search_type == 2:
            should_list.append({"match": {
                "display_name": {
                    "query": and_list[0]['content'],
                    "minimum_should_match": "75%"
                }}})
            should_list.append({"match": {
                "display_name_acronyms": {
                    "query": and_list[0]['content'],
                    "minimum_should_match": "75%"
                }}})
            should_list.append({"match": {
                "country_code": {
                    "query": and_list[0]['content'],
                    "minimum_should_match": "75%"
                }}})
            should_list.append({"match": {
                "institution_type": {
                    "query": and_list[0]['content'],
                    "minimum_should_match": "75%"
                }}})
            should_list.append({"match": {
                "domain": {
                    "query": and_list[0]['content'],
                    "minimum_should_match": "75%"
                }}})
            highlight['fields']['display_name'] = {}
            highlight['fields']['display_name_acronyms'] = {}
            highlight['fields']['country_code'] = {}
            highlight['fields']['institution_type'] = {}
            highlight['fields']['domain'] = {}
        elif search_type == 3:
            should_list.append({"match": {
                "display_name": {
                    "query": and_list[0]['content'],
                    "minimum_should_match": "75%"
                }}})
            should_list.append({"match": {
                "description": {
                    "query": and_list[0]['content'],
                    "minimum_should_match": "75%"
                }}})
            highlight['fields']['display_name'] = {}
            highlight['fields']['description'] = {}
    else:
        for item in and_list:
            if item['select'] == "":
                must_list.append({"query_string": {"query": item['content'], "fields": ["*"],
                                                   }})
                highlight['fields']['*'] = {}
            else:
                if item['clear'] == 1:
                    must_list.append({"match": {
                        com_table[search_type][item['select']]: {
                            "query": item['content'],
                            "minimum_should_match": "75%"
                        }
                    }})
                else:
                    must_list.append({"match": {
                        com_table[search_type][item['select']]: {
                            "query": item['content'],
                            "fuzziness": "AUTO",
                            "minimum_should_match": "75%"
                        }
                    }})
                highlight['fields'][com_table[search_type][item['select']]] = {}
        for item in or_list:
            if item['clear'] == 1:
                should_list.append({"match": {com_table[search_type][item['select']]: {
                    "query": item['content'],
                    "minimum_should_match": "75%"
                }}})
            else:
                should_list.append({"match": {com_table[search_type][item['select']]: {
                    "query": item['content'],
                    "fuzziness": "AUTO",
                    "minimum_should_match": "75%"
                }}})
            highlight['fields'][com_table[search_type][item['select']]] = {}
        for item in not_list:
            if item['clear'] == 1:
                must_not_list.append({"match": {com_table[search_type][item['select']]: {
                    "query": item['content'],
                    "minimum_should_match": "75%"
                }}})
            else:
                must_not_list.append({"match": {com_table[search_type][item['select']]: {
                    "query": item['content'],
                    "fuzziness": "AUTO",
                    "minimum_should_match": "75%"
                }}})
            highlight['fields'][com_table[search_type][item['select']]] = {}
    if search_type == 0:
        paper_deletes = Paper_delete.objects.all()
        for paper_delete in paper_deletes:
            must_not_list.append({"match": {"id": paper_delete.es_id}})
    if search_type == 0 and (start_time != 0 or end_time != 0):
        temp = {}
        if start_time != 0:
            temp["gte"] = start_time
        if end_time != 0:
            temp["lte"] = end_time
        if len(and_list) + len(or_list) + len(not_list) == 1 and and_list[0]['select'] == "":
            search_body = {
                "query": {
                    "bool": {
                        "must": must_list,
                        "should": should_list,
                        "minimum_should_match": "3<75%",
                        "must_not": must_not_list,
                        "filter": [
                            {
                                "range": {
                                    "publication_date": temp
                                }
                            }
                        ],
                    }
                },
                "highlight": highlight
            }
        else:
            search_body = {
                "query": {
                    "bool": {
                        "must": must_list,
                        "should": should_list,
                        "must_not": must_not_list,
                        "filter": [
                            {
                                "range": {
                                    "publication_date": temp
                                }
                            }
                        ],
                    }
                },
                "highlight": highlight
            }
    else:
        search_body = {
            "query": {
                "bool": {
                    "must": must_list,
                    "should": should_list,
                    "must_not": must_not_list,
                    "filter": []
                }
            },
            "highlight": highlight
        }


    return search_body


sort_table = [[
    {
        "cited_count": {
            "order": "desc"
        }
    },
    {
        "cited_count": {
            "order": "asc"
        }
    },
    {
        "publication_date": {
            "order": "desc"
        }
    },
    {
        "publication_date": {
            "order": "asc"
        }
    },
    {
        "title.keyword": {
            "order": "desc"
        }
    },
    {
        "title.keyword": {
            "order": "asc"
        }
    }
], [
    {
        "summary_stats.cited_by_count": {
            "order": "desc"
        }
    },
    {
        "summary_stats.cited_by_count": {
            "order": "asc"
        }
    },
    {
        "summary_stats.h_index": {
            "order": "desc"
        }
    },
    {
        "summary_stats.h_index": {
            "order": "asc"
        }
    },
    {
        "summary_stats.2yr_i10_index": {
            "order": "desc"
        }
    },
    {
        "summary_stats.2yr_i10_index": {
            "order": "asc"
        }
    },
    {
        "summary_stats.works_count": {
            "order": "desc"
        }
    },
    {
        "summary_stats.works_count": {
            "order": "asc"
        }
    },
    {
        "display_name.keyword": {
            "order": "desc"
        }
    },
    {
        "display_name.keyword": {
            "order": "asc"
        }
    }
], [
    {
        "summary_stats.cited_by_count": {
            "order": "desc"
        }
    },
    {
        "summary_stats.cited_by_count": {
            "order": "asc"
        }
    },
    {
        "summary_stats.h_index": {
            "order": "desc"
        }
    },
    {
        "summary_stats.h_index": {
            "order": "asc"
        }
    },
    {
        "summary_stats.2yr_i10_index": {
            "order": "desc"
        }
    },
    {
        "summary_stats.2yr_i10_index": {
            "order": "asc"
        }
    },
    {
        "summary_stats.works_count": {
            "order": "desc"
        }
    },
    {
        "summary_stats.works_count": {
            "order": "asc"
        }
    },
    {
        "display_name.keyword": {
            "order": "desc"
        }
    },
    {
        "display_name.keyword": {
            "order": "asc"
        }
    }
], [
    {
        "summary_stats.h_index": {
            "order": "desc"
        }
    },
    {
        "summary_stats.h_index": {
            "order": "asc"
        }
    },
    {
        "summary_stats.works_count": {
            "order": "desc"
        }
    },
    {
        "summary_stats.works_count": {
            "order": "asc"
        }
    },
    {
        "level": {
            "order": "desc"
        }
    },
    {
        "level": {
            "order": "asc"
        }
    },
    {
        "display_name.keyword": {
            "order": "desc"
        }
    },
    {
        "display_name.keyword": {
            "order": "asc"
        }
    }
]
]
agg_table = [
    {  # works
        "publication_date": {
            "date_histogram": {
                "field": "publication_date",
                # "fixed_interval": "1y"  # 按年聚合
                "calendar_interval": "1y"  # 按年聚合
            }
        }
    },
    {  # author
        "display_name": {  # 聚合作者信息
            "terms": {"field": "display_name.keyword"}
        },
        "institution": {
            "terms": {"field": "institution.keyword"}  # 聚合机构信息
        },
    },
    {  # institution
        "country_code": {  # 聚合作者信息
            "terms": {"field": "country_code.keyword"}
        },
        "type": {
            "terms": {"field": "type.keyword"}  # 聚合期刊信息
        },
        "domain_main": {
            "terms": {"field": "domain_main.keyword"}  # 聚合领域信息
        }
    },
    {
        "level": {
            "terms": {"field": "level"}  # 聚合领域信息
        }
    },
    {  # author
        "domain": {  # 聚合作者信息
            "terms": {
                "script": {
                    "source": """
                            def domainsField = doc["domain.keyword"];
                                  if (domainsField != null && !domainsField.empty) {
                                      def domains = domainsField.value.splitOnToken(' | ');
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
        },
    },
    {  # works
        "author_main": {  # 聚合作者信息
            "terms": {"field": "author_main.keyword"}
        },
    },
    {  # works
        "source": {
            "terms": {"field": "source.keyword"}  # 聚合期刊信息
        },
    },
    {  # works
        "domain_main": {
            "terms": {"field": "domain_main.keyword"}  # 聚合领域信息
        }
    },
    {  # works
        "type_num": {
            "terms": {"field": "type_num"}  # 聚合领域信息
        }
    }
]


def handle_search_list_2(search_body, search_type, first_search, work_clustering,
                         author_clustering, size, from_, sort_):
    search_body["size"] = size
    search_body["from"] = from_
    if sort_ != -1:
        search_body["sort"] = sort_table[search_type][sort_]
    if first_search == 1:
        search_body["aggs"] = agg_table[search_type]
        if search_type == 1 and author_clustering == 1:  # 领域聚合
            search_body["aggs"] = agg_table[4]
        if search_type == 0 and work_clustering == 1:  # 作者聚合
            search_body["aggs"] = agg_table[5]
        if search_type == 0 and work_clustering == 2:  # 来源聚合
            search_body["aggs"] = agg_table[6]
        if search_type == 0 and work_clustering == 3:  # 领域聚合
            search_body["aggs"] = agg_table[7]
        if search_type == 0 and work_clustering == 4:
            search_body["aggs"] = agg_table[8]  # 种类聚合
    return search_body, search_type_table[search_type]


def handle_search_list_3(search_body, extend_list):
    value_list = []
    for i in range(len(extend_list)):
        text = extend_list[i]['text']
        value = extend_list[i]['value']
        if text == "publication_date":
            value_list.append(int(value))
        elif text == "level" or text == "type_num":
            search_body['query']['bool']['filter'].append({"term": {text: value}})
        else:
            search_body['query']['bool']['filter'].append({"term": {text + ".keyword": value}})
        # search_body['highlight']['fields'][text] = {}
    if len(value_list) > 0:
        search_body['query']['bool']['filter'].append({"bool": {"should": [], "minimum_should_match": 1}})
        for i in range(len(value_list)):
            temp = {"gte": str(value_list[i]), "lte": str(value_list[i] + 1)}
            search_body['query']['bool']['filter'][-1]["bool"]['should'].append({"range": {"publication_date": temp}})
    return search_body


def handle_search_result(result, search_type, first_search, work_clustering, author_clustering):
    result_data = {}
    result_data['total'] = result['hits']['total']['value']
    result_data['result'] = []
    if search_type == 0:
        result_data['result'] = paper_handle2(result)
    elif search_type == 1:
        result_data['result'] = author_handle2(result)
    elif search_type == 2:
        result_data['result'] = institution_handle2(result)
    elif search_type == 3:
        result_data['result'] = concept_handle2(result)
    result_data['agg'] = []
    if first_search == 1:
        if search_type == 0:
            if work_clustering == 0:
                work_agg = result['aggregations']['publication_date']['buckets']
                result_data['agg'].append({'name': 'Publication Date', 'text': 'publication_date', 'data': []})
                for item in work_agg:
                    # iso_date = datetime.fromisoformat(item['key_as_string'][:-1])
                    # time0 = iso_date.strftime("%Y")
                    # result_data['agg'][0]['data'].append({'time': time0, 'value': item['doc_count']})
                    iso_date = datetime.fromisoformat(item['key_as_string'][:-1])
                    time0 = iso_date.strftime("%Y")
                    if item['doc_count'] > 0:
                        result_data['agg'][0]['data'].append({'raw': time0,
                                                              'value': item['doc_count']})
            if work_clustering == 1:
                work_agg = result['aggregations']['author_main']['buckets']
                result_data['agg'].append({'name': 'Main Author', 'text': 'author_main', 'data': []})
                for item in work_agg:
                    # temp = item['key'].split(' | ')[0]
                    # temp = temp.split(' & ')
                    # result_data['agg'][0]['data'].append({'name': temp[0], 'id': temp[1], 'value': item['doc_count']})
                    if item['doc_count'] > 0:
                        result_data['agg'][0]['data'].append({'raw': item['key'], 'value': item['doc_count']})
            if work_clustering == 2:
                work_agg = result['aggregations']['source']['buckets']
                result_data['agg'].append({'name': 'Source', 'text': 'source', 'data': []})
                for item in work_agg:
                    # temp = item['key'].split(' | ')[0]
                    # temp = temp.split(' & ')
                    # result_data['agg'][0]['data'].append({'name': temp[0], 'type': temp[1],
                    #                                       'id': temp[2], 'value': item['doc_count']})
                    if item['doc_count'] > 0:
                        result_data['agg'][0]['data'].append({'raw': item['key'], 'value': item['doc_count']})
            if work_clustering == 3:
                work_agg = result['aggregations']['domain_main']['buckets']
                result_data['agg'].append({'name': 'Main Domain', 'text': 'domain_main', 'data': []})
                for item in work_agg:
                    # temp = item['key'].split(' | ')[0]
                    # temp = temp.split(' & ')
                    # result_data['agg'][0]['data'].append({'name': temp[0], 'id': temp[1],
                    #                                       'level': temp[2], 'value': item['doc_count']})
                    if item['doc_count'] > 0:
                        result_data['agg'][0]['data'].append({'raw': item['key'], 'value': item['doc_count']})
            if work_clustering == 4:
                work_agg = result['aggregations']['type_num']['buckets']
                result_data['agg'].append({'name': 'Type', 'text': 'type_num', 'data': []})
                for item in work_agg:
                    # result_data['agg'][0]['data'].append({'name': item['key'], 'value': item['doc_count']})
                    if item['doc_count'] > 0:
                        result_data['agg'][0]['data'].append({'raw': item['key'], 'value': item['doc_count']})
        elif search_type == 1:
            if author_clustering == 0:
                author_agg = result['aggregations']['display_name']['buckets']
                result_data['agg'].append({'name': 'Name', 'text': 'display_name', 'data': []})
                for item in author_agg:
                    # temp = item['key'].split(' & ')
                    # result_data['agg'][0]['data'].append({'name': temp[0], 'id': temp[1], 'value': item['doc_count']})
                    if item['doc_count'] > 0:
                        result_data['agg'][0]['data'].append({'raw': item['key'], 'value': item['doc_count']})
                institution_agg = result['aggregations']['institution']['buckets']
                result_data['agg'].append({'name': 'Institution', 'text': 'institution', 'data': []})
                for item in institution_agg:
                    # temp = item['key'].split(' | ')[0]
                    # temp = temp.split(' & ')
                    # result_data['agg'][1]['data'].append({'name': temp[0], 'id': temp[1], 'type': temp[2],
                    #                                       'value': item['doc_count']})
                    if item['doc_count'] > 0:
                        result_data['agg'][1]['data'].append({'raw': item['key'], 'value': item['doc_count']})
            if author_clustering == 1:
                author_agg = result['aggregations']['domain']['buckets']
                result_data['agg'].append({'name': 'Domain', 'text': 'domain', 'data': []})
                for item in author_agg:
                    # temp = item['key'].split(' | ')[0]
                    # temp = temp.split(' & ')
                    # result_data['agg'][0]['data'].append({'name': temp[0], 'id': temp[1],
                    #                                       'level': temp[2], 'value': item['doc_count']})
                    if item['doc_count'] > 0:
                        result_data['agg'][0]['data'].append({'raw': item['key'], 'value': item['doc_count']})
        elif search_type == 2:
            institution_agg = result['aggregations']['country_code']['buckets']
            result_data['agg'].append({'name': 'Country Code', 'text': 'country_code', 'data': []})
            for item in institution_agg:
                # result_data['agg'][0]['data'].append({'name': item['key'], 'value': item['doc_count']})
                if item['doc_count'] > 0:
                    result_data['agg'][0]['data'].append({'raw': item['key'], 'value': item['doc_count']})
            institution_agg = result['aggregations']['type']['buckets']
            result_data['agg'].append({'name': 'Institution Type', 'text': 'type', 'data': []})
            for item in institution_agg:
                # result_data['agg'][1]['data'].append({'name': item['key'], 'value': item['doc_count']})
                if item['doc_count'] > 0:
                    result_data['agg'][1]['data'].append({'raw': item['key'], 'value': item['doc_count']})
            institution_agg = result['aggregations']['domain_main']['buckets']
            result_data['agg'].append({'name': 'Main Domain', 'text': 'domain_main', 'data': []})
            for item in institution_agg:
                # temp = item['key'].split(' | ')[0]
                # temp = temp.split(' & ')
                # result_data['agg'][2]['data'].append({'name': temp[0], 'id': temp[1],
                #                                       'level': temp[2], 'value': item['doc_count']})
                if item['doc_count'] > 0:
                    result_data['agg'][2]['data'].append({'raw': item['key'], 'value': item['doc_count']})
        elif search_type == 3:
            concept_agg = result['aggregations']['level']['buckets']
            result_data['agg'].append({'name': 'Level', 'text': 'level', 'data': []})
            for item in concept_agg:
                # result_data['agg'][0]['data'].append({'name': item['key'], 'value': item['doc_count']})
                if item['doc_count'] > 0:
                    result_data['agg'][0]['data'].append({'raw': item['key'], 'value': item['doc_count']})
        for i in range(len(result_data['agg'])):
            if len(result_data['agg'][i]['data']) > 0:
                result_data['agg'][i]['data'].sort(key=lambda x: x['value'], reverse=True)
    return result_data


def handle_corresponding_author_ids(corresponding_author_ids):
    if len(corresponding_author_ids) == 0:
        return []
    search_body = {
        "query": {
            "bool": {
                "must": [
                    {
                        "terms": {
                            "id": corresponding_author_ids
                        }
                    }
                ]
            }
        }
    }
    result = es_search.body_search("authors", search_body)
    result = author_handle(result)
    return result


def handle_corresponding_institutions_ids(corresponding_institutions_ids):
    if len(corresponding_institutions_ids) == 0:
        return []
    search_body = {
        "query": {
            "bool": {
                "must": [
                    {
                        "terms": {
                            "id": corresponding_institutions_ids
                        }
                    }
                ]
            }
        }
    }
    result = es_search.body_search("institutions", search_body)
    result = hot_institution_handle(result)
    return result


def handle_referenced_works(referenced_works):
    if len(referenced_works) == 0:
        return []
    search_body = {
        "query": {
            "bool": {
                "must": [
                    {
                        "terms": {
                            "id": referenced_works
                        }
                    }
                ]
            }
        }
    }
    result = es_search.body_search("works", search_body)
    result = hot_paper_handle(result)
    return result


def handle_related_works(related_works):
    if len(related_works) == 0:
        return []
    search_body = {
        "query": {
            "bool": {
                "must": [
                    {
                        "terms": {
                            "id": related_works
                        }
                    }
                ]
            }
        }
    }
    result = es_search.body_search("works", search_body)
    result = hot_paper_handle(result)
    return result


def handle_associated_institutions(associated_institutions):
    associated_institutions0 = {"parent": [], "child": [], "related": []}
    if len(associated_institutions) == 0:
        return associated_institutions0
    for institution in associated_institutions:
        try:
            del institution['lineage']
        except:
            pass
        institution['id'] = institution['id'].split('https://openalex.org/I')[1]
        associated_institutions0[institution['relationship']].append(institution)
    return associated_institutions0


def handle_detailed_work(result):
    result_data = {}
    result_data['title'] = result['_source']['title']
    result_data['id'] = result['_source']['id']
    result_data['abstract'] = result['_source'].get('abstract', "")
    result_data['cited_count'] = result['_source']['cited_count']
    result_data['domain'] = domain_field_handle(result['_source']['domain'])
    result_data['author_all'] = author_all_field_handle(result['_source'].get('author_all', ""))
    result_data['pdf_url'] = result['_source'].get('pdf_url', "")
    result_data['landing_page_url'] = result['_source'].get('landing_page_url', "")
    result_data['source'] = source_field_handle(result['_source'].get('source', ""))
    result_data['publication_date'] = result['_source']['publication_date']
    result_data['type_num'] = result['_source']['type_num']
    result_data['counts_by_year'] = result['_source'].get('counts_by_year', [])
    result_data['corresponding_author'] = (
        handle_corresponding_author_ids(result['_source'].get('corresponding_author_ids', [])))
    result_data['corresponding_institutions'] = (
        handle_corresponding_institutions_ids(result['_source'].get('corresponding_institutions_ids', [])))
    result_data['referenced_works'] = handle_referenced_works(result['_source'].get('referenced_works', []))
    result_data['related_works'] = handle_related_works(result['_source'].get('related_works', []))
    return result_data


def handle_detailed_author(result):
    result_data = {}
    result_data['display_name'] = result['_source']['display_name']
    result_data['domain'] = domain_field_handle(result['_source']['domain'])
    result_data['institution'] = institution_field_handle(result['_source'].get('institution', ""))
    result_data['most_cited_work'] = result['_source'].get('most_cited_work', "")
    result_data['cited_by_count'] = result['_source']['cited_by_count']
    result_data['summary_stats'] = handle_summary_stats(result['_source']['summary_stats'])
    result_data['id'] = result['_source']['id']
    result_data['orcid'] = result['_source'].get('orcid', "")
    result_data['counts_by_year'] = result['_source'].get('counts_by_year', [])
    if Scholar.objects.filter(es_id=result_data['id'], claimed_user_id__isnull=False).exists():
        result_data['claimed'] = True
    else:
        result_data['claimed'] = False
    return result_data


def handle_detailed_institution(result):
    result_data = {}
    result_data['display_name'] = result['_source']['display_name']
    result_data['display_name_acronyms'] = result['_source'].get('display_name_acronyms', "")
    result_data['country_code'] = result['_source'].get('country_code', "")
    result_data['image_url'] = result['_source'].get('image_url', "")
    result_data['id'] = result['_source']['id']
    result_data['summary_stats'] = handle_summary_stats(result['_source']['summary_stats'])
    result_data['homepage_url'] = result['_source'].get('homepage_url', "")
    result_data['type'] = result['_source'].get('type', "")
    result_data['domain'] = domain_field_handle(result['_source']['domain'])
    result_data['geo'] = result['_source'].get('geo', "")
    result_data['ror'] = result['_source'].get('ror', "")
    result_data['counts_by_year'] = result['_source'].get('counts_by_year', [])
    result_data['associated_institutions'] = (
        handle_associated_institutions(result['_source'].get('associated_institutions', [])))
    return result_data


def handle_detailed_concept(result):
    result_data = {}
    result_data['display_name'] = result['_source']['display_name']
    result_data['description'] = result['_source'].get('description', "")
    result_data['id'] = result['_source']['id']
    result_data['summary_stats'] = handle_summary_stats(result['_source']['summary_stats'])
    result_data['level'] = result['_source']['level']
    result_data['image_url'] = result['_source'].get('image_url', "")
    result_data['ancestors'] = result['_source'].get('ancestors', "")
    result_data['sons'] = result['_source'].get('sons', "")
    result_data['counts_by_year'] = result['_source'].get('counts_by_year', [])
    return result_data


def star_handle(result, user, search_type):
    if user is None or user is False:
        for item in result:
            item['is_star'] = False
        return result
    for item in result:
        if Star.objects.filter(user=user, paper_id=item['id'], type=search_type).exists():
            item['is_star'] = True
        else:
            item['is_star'] = False
    return result


def handle_network(result, author_id):
    if len(result) == 0:
        return {
            'co_work_list': [],
            'refer_list': [],
            'referred_list': []
        }
    paper_list = []
    refer_paper_list = []
    co_work_list = []
    refer_list = []
    referred_list = []
    for item in result:
        paper_list.append(item['_source']['id'])
        refer_paper_list += item['_source'].get('referenced_works', [])
        co_work_list += author_all_field_handle(item['_source'].get('author_all', ""))
    refer_paper_list = list(set(refer_paper_list))
    temp_dict = {}
    for item in co_work_list:
        if item['id'] != author_id:
            try:
                temp_dict[item['id']]['count'] += 1
            except:
                temp_dict[item['id']] = item
                temp_dict[item['id']]['count'] = 1
    co_work_list = []
    for item in temp_dict:
        co_work_list.append(temp_dict[item])
    search_body = {
        "query": {
            "terms": {
                "id": refer_paper_list
            }
        }
    }
    result = es_search.body_search("works", search_body)
    for item in result['hits']['hits']:
        refer_list += author_all_field_handle(item['_source'].get('author_all', ""))
    temp_dict = {}
    for item in refer_list:
        if item['id'] != author_id:
            try:
                temp_dict[item['id']]['count'] += 1
            except:
                temp_dict[item['id']] = item
                temp_dict[item['id']]['count'] = 1
    refer_list = []
    for item in temp_dict:
        refer_list.append(temp_dict[item])
    search_body = {
        "query": {
            "terms": {
                "referenced_works": paper_list
            }
        }
    }
    result = es_search.body_search("works", search_body)
    for item in result['hits']['hits']:
        referred_list += author_all_field_handle(item['_source'].get('author_all', ""))
    temp_dict = {}
    for item in referred_list:
        if item['id'] != author_id:
            try:
                temp_dict[item['id']]['count'] += 1
            except:
                temp_dict[item['id']] = item
                temp_dict[item['id']]['count'] = 1
    referred_list = []
    for item in temp_dict:
        referred_list.append(temp_dict[item])
    co_work_list.sort(key=lambda x: x['count'], reverse=True)
    refer_list.sort(key=lambda x: x['count'], reverse=True)
    referred_list.sort(key=lambda x: x['count'], reverse=True)
    return {
        'co_work_list': co_work_list,
        'refer_list': refer_list,
        'referred_list': referred_list
    }


def handle_summary_stats(summary_stats):
    summary_stats0 = {}
    for key, value in summary_stats.items():
        if key == "2yr_i10_index":
            summary_stats0['yr2_i10_index'] = value
        elif key == "2yr_mean_citedness":
            summary_stats0['yr2_mean_citedness'] = value
        elif key == "2yr_works_count":
            summary_stats0['yr2_works_count'] = value
        elif key == "2yr_cited_by_count":
            summary_stats0['yr2_cited_by_count'] = value
        elif key == "2yr_h_index":
            summary_stats0['yr2_h_index'] = value
        else:
            summary_stats0[key] = value
    return summary_stats0
