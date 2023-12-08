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

def search(request):
    if request.method != "POST":
        return JsonResponse({'errno': 1001, 'errmsg': '请求方法错误'})
    body = json.loads(request.body)
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
    if start_time is None:
        start_time = 0
    end_time = body.get('end_time')
    if end_time is None:
        end_time = 0
    search_body = es_handle.handle_search_list_1(search_type, and_list, or_list, not_list, start_time, end_time)



