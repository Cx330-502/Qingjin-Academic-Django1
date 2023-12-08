def author_all_handle(author_all):
    author_list = []
    authors = author_all.split('|')
    for author_info in authors:
        # 按照 "&" 分割不同字段
        author_fields = [field.strip() for field in author_info.split('&') if field.strip()]
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


def domain_handle(domain):
    domain_list = []
    domains = domain.split('|')
    for domain_info in domains:
        # 按照 "&" 分割不同字段
        domain_fields = [field.strip() for field in domain_info.split('&') if field.strip()]

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


def hot_paper_handle(result):
    result_data = []
    for hit0 in result['hits']['hits']:
        hit = {}
        hit['title'] = hit0['_source']['title']
        hit['id'] = hit0['_source']['id']
        hit['cited_count'] = hit0['_source']['cited_count']
        hit['author_all'] = author_all_handle(hit0['_source']['author_all'])
        hit['publication_date'] = hit0['_source']['publication_date']
        result_data.append(hit)
    return result_data


def hot_institution_handle(result):
    result_data = []
    for hit0 in result['hits']['hits']:
        hit = {}
        hit['display_name'] = hit0['_source']['display_name']
        hit['id'] = hit0['_source']['id']
        hit['image_url'] = hit0['_source']['image_url']
        hit['ror'] = hit0['_source']['ror']
        hit['summary_stats'] = hit0['_source']['summary_stats']
        result_data.append(hit)
    return result_data


def author_handle(result_1):
    result_data = []
    for hit0 in result_1['hits']['hits']:
        hit = {}
        hit['display_name'] = hit0['_source']['display_name']
        hit['id'] = hit0['_source']['id']
        hit['most_cited_work'] = hit0['_source']['most_cited_work']
        hit['cited_by_count'] = hit0['_source']['cited_by_count']
        hit['summary_stats'] = hit0['_source']['summary_stats']
        hit['orcid'] = hit0['_source']['orcid']
        result_data.append(hit)
    return result_data


def concept_handle(result_3):
    result_data = []
    for hit0 in result_3['hits']['hits']:
        hit = {}
        hit['display_name'] = hit0['_source']['display_name']
        hit['id'] = hit0['_source']['id']
        hit['description'] = hit0['_source']['description']
        hit['summary_stats'] = hit0['_source']['summary_stats']
        hit['level'] = hit0['_source']['level']
        hit['image_url'] = hit0['_source']['image_url']
        result_data.append(hit)
    return result_data


search_type_table = ['works', 'institutions', 'authors', 'concepts']
com_table = [{
    '标题': 'title',
    '摘要': 'abstract',
    '领域': 'domain',
    '作者': 'author_all',
    '来源': 'source',
    '第一作者': 'main_author',
    '主要领域': 'main_domain',
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
    '主要领域': 'main_domain',
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
    if len(and_list) + len(or_list) + len(not_list) == 1 and and_list[0]['select'] == "":
        must_list.append({"match": {"*": {"query": and_list[0]['content'], "fuzziness": "AUTO"}}})
    else:
        for item in and_list:
            if item['clear'] == 1:
                must_list.append({"match": {com_table[search_type][item['select']]: item['content']}})
            else:
                must_list.append({"match": {com_table[search_type][item['select']]: {"query": item['content'],
                                                                                     "fuzziness": "AUTO"}}})
        for item in or_list:
            if item['clear'] == 1:
                should_list.append({"match": {com_table[search_type][item['select']]: item['content']}})
            else:
                should_list.append({"match": {com_table[search_type][item['select']]: {"query": item['content'],
                                                                                       "fuzziness": "AUTO"}}})
        for item in not_list:
            if item['clear'] == 1:
                must_not_list.append({"match": {com_table[search_type][item['select']]: item['content']}})
            else:
                must_not_list.append({"match": {com_table[search_type][item['select']]: {"query": item['content'],
                                                                                         "fuzziness": "AUTO"}}})
    if search_type == 0 and ( start_time != 0 or end_time != 0):
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
                    "filter": {
                        "range": {
                            "publication_date": temp
                        }
                    }
                }
            }
        }
    else:
        search_body = {
            "query": {
                "bool": {
                    "must": must_list,
                    "should": should_list,
                    "must_not": must_not_list
                }
            }
        }
    return search_body
