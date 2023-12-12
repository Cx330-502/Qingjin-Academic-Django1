import datetime
import random
import base64
import re
import Home.extra_codes.captcha as captchaClass
import ES_scripts.es_search_script as es_search
import ES_scripts.es_handle_script as es_handle
import hashlib

from django.conf import settings
from Academic_models.models import *
from django.core.exceptions import ValidationError
from django.core.files import File
from django.core.validators import validate_email
from django.http import JsonResponse
import json


# Create your views here.

def search0(request):
    if request.method != "POST":
        return JsonResponse({'errno': 1001, 'errmsg': '请求方法错误'})
    body = json.loads(request.body)
    user = auth_token(body.get('token'), False)
    search_type = body.get('search_type')
    if search_type is None:
        return JsonResponse({'errno': 1002, 'errmsg': '缺少搜索类型'})
    if search_type < 0 or search_type > 3:
        return JsonResponse({'errno': 1003, 'errmsg': '搜索类型错误'})
    and_list = body.get('and_list')
    if and_list is None or len(and_list) == 0:
        return JsonResponse({'errno': 1004, 'errmsg': '缺少搜索条件'})
    or_list = body.get('or_list')
    if or_list is None:
        or_list = []
    not_list = body.get('not_list')
    if not_list is None:
        not_list = []
    start_time = body.get('start_time')
    if start_time is None or start_time == "":
        start_time = 0
    end_time = body.get('end_time')
    if end_time is None or end_time == "":
        end_time = 0
    search_body = es_handle.handle_search_list_1(search_type, and_list, or_list, not_list, start_time, end_time)
    first_search = body.get('first_search')
    if first_search is None:
        first_search = 1
    work_clustering = body.get('work_clustering')
    if work_clustering is None:
        work_clustering = 0
    author_clustering = body.get('author_clustering')
    if author_clustering is None:
        author_clustering = 0
    size = body.get('size')
    if size is None:
        size = 20
    from_ = body.get('from')
    if from_ is None:
        from_ = 0
    sort_ = body.get('sort')
    if sort_ is None:
        sort_ = -1
    search_body, search_type0 = es_handle.handle_search_list_2(search_body, search_type, first_search,
                                                               work_clustering, author_clustering, size, from_, sort_)
    extend_list = body.get('extend_list')
    if extend_list is None:
        extend_list = []
    if len(extend_list) > 0:
        search_body = es_handle.handle_search_list_3(search_body, extend_list)
    time0 = datetime.datetime.now()
    result = es_search.body_search(search_type0, search_body)
    print(datetime.datetime.now() - time0)
    result = es_handle.handle_search_result(result, search_type, first_search, work_clustering, work_clustering)
    result['result'] = es_handle.star_handle(result['result'], user, search_type)
    return JsonResponse({'errno': 0, 'errmsg': 'success', 'data': result})
