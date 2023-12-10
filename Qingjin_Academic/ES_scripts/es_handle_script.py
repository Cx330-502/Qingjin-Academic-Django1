from datetime import datetime


def author_all_field_handle(author_all):
    if author_all == '' or author_all is None:
        return []
    author_list = []
    authors = author_all.split(' | ')
    for author_info in authors:
        if author_info == '':
            continue
        # 按照 "&" 分割不同字段
        author_fields = [field.strip() for field in author_info.split(' & ') if field.strip()]
        if len(author_fields) < 2:
            continue
        # 将字段组成字典
        author_dict = {
            "name": author_fields[0],  # 第一个字段为姓名
            "id": author_fields[1]  # 第二个字段为ID（假设有两个字段）
        }

        # 将每个作者的信息添加到列表中
        author_list.append(author_dict)
    return author_list


def domain_field_handle(domain):
    if domain == '' or domain is None:
        return []
    domain_list = []
    domains = domain.split(' | ')
    for domain_info in domains:
        if domain_info == '':
            continue
        # 按照 "&" 分割不同字段
        domain_fields = [field.strip() for field in domain_info.split(' & ') if field.strip()]
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
    print(institution)
    institutions = institution.split(' | ')
    for institution_info in institutions:
        if institution_info == '':
            continue
        # 按照 "&" 分割不同字段
        institution_fields = [field.strip() for field in institution_info.split(' & ') if field.strip()]
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
    sources = source.split(' | ')
    for source_info in sources:
        if source_info == '':
            continue
        # 按照 "&" 分割不同字段
        source_fields = [field.strip() for field in source_info.split(' & ') if field.strip()]
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
        hit['summary_stats'] = hit0['_source']['summary_stats']
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
        hit['summary_stats'] = hit0['_source']['summary_stats']
        hit['orcid'] = hit0['_source'].get('orcid', "")
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
        hit['summary_stats'] = hit0['_source']['summary_stats']
        hit['level'] = hit0['_source']['level']
        hit['image_url'] = hit0['_source'].get('image_url', "")
        result_data.append(hit)
    return result_data


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
        hit['id'] = hit0['_source']['id']
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
        hit['id'] = hit0['_source']['id']
        hit['summary_stats'] = hit0['_source']['summary_stats']
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
        hit['summary_stats'] = hit0['_source']['summary_stats']
        hit['id'] = hit0['_source']['id']
        hit['orcid'] = hit0['_source'].get('orcid', "")
        result_data.append(hit)
    return result_data


def concept_handle2(result_3):
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
        hit['id'] = hit0['_source']['id']
        hit['summary_stats'] = hit0['_source']['summary_stats']
        hit['level'] = hit0['_source']['level']
        hit['image_url'] = hit0['_source'].get('image_url', "")
        hit['ancestors'] = hit0['_source'].get('ancestors', "")
        result_data.append(hit)
    return result_data


search_type_table = ['works', 'authors', 'institutions', 'concepts']
com_table = [{
    '标题': 'title',
    '摘要': 'abstract',
    '领域': 'domain',
    '作者': 'author_all',
    '来源': 'source',
    '第一作者': 'author_main',
    '主要领域': 'domain_main',
}, {
    '姓名': 'display_name',
    '领域': 'domain',
    '所在机构': 'institution',
    '代表作': 'most_cited_work',
    'orcid': 'orcid',
}, {
    '名字': 'display_name',
    '简称': 'display_name_acronyms',
    '国家编码': 'country_code',
    '机构类型': 'institution_type',
    '领域': 'domain',
    '主要领域': 'domain_main',
    'ror': 'ror',
}, {
    '名字': 'display_name',
    '描述': 'description',
    '学科等级': 'level',
}
]


def handle_search_list_1(search_type, and_list, or_list, not_list, start_time, end_time):
    must_list = []
    should_list = []
    must_not_list = []
    highlight = {"fields": {}}
    if len(and_list) + len(or_list) + len(not_list) == 1 and and_list[0]['select'] == "":
        must_list.append({"query_string": {"query": and_list[0]['content'], "fields": ["*"]}})
        highlight['fields']['*'] = {}
    else:
        for item in and_list:
            if item['clear'] == 1:
                must_list.append({"match": {com_table[search_type][item['select']]: item['content']}})
            else:
                must_list.append({"match": {com_table[search_type][item['select']]: {"query": item['content'],
                                                                                     "fuzziness": "AUTO"}}})
            highlight['fields'][com_table[search_type][item['select']]] = {}
        for item in or_list:
            if item['clear'] == 1:
                should_list.append({"match": {com_table[search_type][item['select']]: item['content']}})
            else:
                should_list.append({"match": {com_table[search_type][item['select']]: {"query": item['content'],
                                                                                       "fuzziness": "AUTO"}}})
            highlight['fields'][com_table[search_type][item['select']]] = {}
        for item in not_list:
            if item['clear'] == 1:
                must_not_list.append({"match": {com_table[search_type][item['select']]: item['content']}})
            else:
                must_not_list.append({"match": {com_table[search_type][item['select']]: {"query": item['content'],
                                                                                         "fuzziness": "AUTO"}}})
            highlight['fields'][com_table[search_type][item['select']]] = {}
    if search_type == 0 and (start_time != 0 or end_time != 0):
        temp = {}
        if start_time != 0:
            temp["gte"] = start_time
        if end_time != 0:
            temp["lte"] = end_time
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
                    ]
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
        "title": {
            "order": "desc"
        }
    },
    {
        "title": {
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
        "display_name": {
            "order": "desc"
        }
    },
    {
        "display_name": {
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
        "display_name": {
            "order": "desc"
        }
    },
    {
        "display_name": {
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
        "display_name": {
            "order": "desc"
        }
    },
    {
        "display_name": {
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
            "terms": {"field": "level.keyword"}  # 聚合领域信息
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
    return search_body, search_type_table[search_type]


def handle_search_list_3(search_body, extend_list):
    value_list = []
    for i in range(len(extend_list)):
        text = extend_list[i]['text']
        value = extend_list[i]['value']
        if text == "publication_date":
            value_list.append(value)
        else:
            search_body['query']['bool']['filter'].append({"term": {text: value}})
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
                result_data['agg'].append({'name': '发表时间', 'text': 'publication_date', 'data': []})
                for item in work_agg:
                    # iso_date = datetime.fromisoformat(item['key_as_string'][:-1])
                    # time0 = iso_date.strftime("%Y")
                    # result_data['agg'][0]['data'].append({'time': time0, 'value': item['doc_count']})
                    iso_date = datetime.fromisoformat(item['key_as_string'][:-1])
                    time0 = iso_date.strftime("%Y")
                    result_data['agg'][0]['data'].append({'time': time0,
                                                          'value': item['doc_count']})
            if work_clustering == 1:
                work_agg = result['aggregations']['author_main']['buckets']
                result_data['agg'].append({'name': '主要作者', 'text': 'author_main', 'data': []})
                for item in work_agg:
                    # temp = item['key'].split(' | ')[0]
                    # temp = temp.split(' & ')
                    # result_data['agg'][0]['data'].append({'name': temp[0], 'id': temp[1], 'value': item['doc_count']})
                    result_data['agg'][0]['data'].append({'raw': item['key'], 'value': item['doc_count']})
            if work_clustering == 2:
                work_agg = result['aggregations']['source']['buckets']
                result_data['agg'].append({'name': '来源', 'source': 'source', 'data': []})
                for item in work_agg:
                    # temp = item['key'].split(' | ')[0]
                    # temp = temp.split(' & ')
                    # result_data['agg'][0]['data'].append({'name': temp[0], 'type': temp[1],
                    #                                       'id': temp[2], 'value': item['doc_count']})
                    result_data['agg'][0]['data'].append({'raw': item['key'], 'value': item['doc_count']})
            if work_clustering == 3:
                work_agg = result['aggregations']['domain_main']['buckets']
                result_data['agg'].append({'name': '主要领域', 'text': 'domain_main', 'data': []})
                for item in work_agg:
                    # temp = item['key'].split(' | ')[0]
                    # temp = temp.split(' & ')
                    # result_data['agg'][0]['data'].append({'name': temp[0], 'id': temp[1],
                    #                                       'level': temp[2], 'value': item['doc_count']})
                    result_data['agg'][0]['data'].append({'raw': item['key'], 'value': item['doc_count']})
        elif search_type == 1:
            if author_clustering == 0:
                author_agg = result['aggregations']['display_name']['buckets']
                result_data['agg'].append({'name': '作者', 'text': 'display_name', 'data': []})
                for item in author_agg:
                    # temp = item['key'].split(' & ')
                    # result_data['agg'][0]['data'].append({'name': temp[0], 'id': temp[1], 'value': item['doc_count']})
                    result_data['agg'][0]['data'].append({'raw': item['key'], 'value': item['doc_count']})
                institution_agg = result['aggregations']['institution']['buckets']
                result_data['agg'].append({'name': '机构', 'text': 'institution', 'data': []})
                for item in institution_agg:
                    # temp = item['key'].split(' | ')[0]
                    # temp = temp.split(' & ')
                    # result_data['agg'][1]['data'].append({'name': temp[0], 'id': temp[1], 'type': temp[2],
                    #                                       'value': item['doc_count']})
                    result_data['agg'][1]['data'].append({'raw': item['key'], 'value': item['doc_count']})
            if author_clustering == 1:
                author_agg = result['aggregations']['domain']['buckets']
                result_data['agg'].append({'name': '领域', 'text': 'domain', 'data': []})
                for item in author_agg:
                    # temp = item['key'].split(' | ')[0]
                    # temp = temp.split(' & ')
                    # result_data['agg'][0]['data'].append({'name': temp[0], 'id': temp[1],
                    #                                       'level': temp[2], 'value': item['doc_count']})
                    result_data['agg'][0]['data'].append({'raw': item['key'], 'value': item['doc_count']})
        elif search_type == 2:
            institution_agg = result['aggregations']['country_code']['buckets']
            result_data['agg'].append({'name': '国家', 'text': 'country_code', 'data': []})
            for item in institution_agg:
                # result_data['agg'][0]['data'].append({'name': item['key'], 'value': item['doc_count']})
                result_data['agg'][0]['data'].append({'raw': item['key'], 'value': item['doc_count']})
            institution_agg = result['aggregations']['type']['buckets']
            result_data['agg'].append({'name': '机构类型', 'text': 'type', 'data': []})
            for item in institution_agg:
                # result_data['agg'][1]['data'].append({'name': item['key'], 'value': item['doc_count']})
                result_data['agg'][1]['data'].append({'raw': item['key'], 'value': item['doc_count']})
            institution_agg = result['aggregations']['domain_main']['buckets']
            result_data['agg'].append({'name': '主要领域', 'text': 'domain_main', 'data': []})
            for item in institution_agg:
                # temp = item['key'].split(' | ')[0]
                # temp = temp.split(' & ')
                # result_data['agg'][2]['data'].append({'name': temp[0], 'id': temp[1],
                #                                       'level': temp[2], 'value': item['doc_count']})
                result_data['agg'][2]['data'].append({'raw': item['key'], 'value': item['doc_count']})
        elif search_type == 3:
            concept_agg = result['aggregations']['level']['buckets']
            result_data['agg'].append({'name': '学科等级', 'text': 'level', 'data': []})
            for item in concept_agg:
                # result_data['agg'][0]['data'].append({'name': item['key'], 'value': item['doc_count']})
                result_data['agg'][0]['data'].append({'raw': item['key'], 'value': item['doc_count']})
    return result_data
