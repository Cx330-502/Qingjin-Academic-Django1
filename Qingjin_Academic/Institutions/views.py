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

def get_institution_information(request):
    if request.method != "POST":
        return JsonResponse({'errno': 1001, 'errmsg': '请求方法错误'})
    body = json.loads(request.body)
    user = auth_token(body.get('token'), False)
    institution_id = body.get("institution_id")
    if institution_id is None or institution_id == "":
        return JsonResponse({'errno': 1002, 'errmsg': '请传入合法的机构id'})
    search_body = {
        "query": {
            "match": {
                "id": institution_id
            }
        }
    }
    result = es_search.body_search("institutions", search_body)
    if len(result['hits']['hits']) == 0:
        return JsonResponse({'errno': 1003, 'errmsg': '机构不存在'})
    result = es_handle.handle_detailed_institution(result['hits']['hits'][0])
    result = es_handle.star_handle([result], user, 2)[0]
    return JsonResponse({'errno': 0,
                         'errmsg': '获取机构信息成功',
                         'data': result})



def get_concept_information(request):
    if request.method != "POST":
        return JsonResponse({'errno': 1001, 'errmsg': '请求方法错误'})
    body = json.loads(request.body)
    user = auth_token(body.get('token'), False)
    concept_id = body.get("concept_id")
    if concept_id is None or concept_id == "":
        return JsonResponse({'errno': 1002, 'errmsg': '请传入合法的概念id'})
    search_body = {
        "query": {
            "match": {
                "id": concept_id
            }
        }
    }
    result = es_search.body_search("concepts", search_body)
    if len(result['hits']['hits']) == 0:
        return JsonResponse({'errno': 1003, 'errmsg': '概念不存在'})
    result = es_handle.handle_detailed_concept(result['hits']['hits'][0])
    result = es_handle.star_handle([result], user, 3)[0]
    return JsonResponse({'errno': 0,
                         'errmsg': '获取概念信息成功',
                         'data': result})
