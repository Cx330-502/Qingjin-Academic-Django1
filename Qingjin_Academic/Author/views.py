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


def email_claim(request):
    if request.method != "POST":
        return JsonResponse({'errno': 1001, 'errmsg': '请求方法错误'})
    body = json.loads(request.body)
    user = auth_token(body.get("token"), False)
    if user is None or user is False:
        return JsonResponse({'errno': 1002, 'errmsg': '登录错误'})
    email = body.get("email")
    if email is None:
        return JsonResponse({'errno': 1003, 'errmsg': '缺少邮箱'})
    domain = email.split("@")
    if len(domain) != 2:
        return JsonResponse({'errno': 1004, 'errmsg': '邮箱格式错误'})
    domain = domain[1]
    domain = domain.split(".")
    if len(domain) < 2:
        return JsonResponse({'errno': 1005, 'errmsg': '邮箱格式错误'})
    author_id = body.get("author_id")
    if author_id is None:
        return JsonResponse({'errno': 1006, 'errmsg': '缺少作者id'})
    if Scholar.objects.filter(es_id=author_id, claimed_user_id__isnull=False).exists():
        return JsonResponse({'errno': 1007, 'errmsg': '作者已被认领'})
    temp = len(domain)
    file_path = "./Author/domains"
    while temp > 0:
        file_path += "/" + domain[temp - 1]
        temp -= 1
    file_path += ".txt"
    print(file_path)
    if not os.path.exists(file_path):
        return JsonResponse({'errno': 1008, 'errmsg': '邮箱不是科研机构邮箱'})
    with open(file_path, "r", encoding="utf-8") as f:
        data0 = f.read()
        data0 = data0[:-1]
    if not user.claimed_scholar is None:
        return JsonResponse({'errno': 1009, 'errmsg': '用户已认领作者'})
    scholar = None
    if Scholar.objects.filter(es_id=author_id).exists():
        scholar = Scholar.objects.get(es_id=author_id)
    else:
        search_body = {
            "query": {
                "match": {
                    "id": author_id
                }
            }
        }
        result = es_search.body_search("authors", search_body)
        if len(result["hits"]["hits"]) == 0:
            return JsonResponse({'errno': 1010, 'errmsg': '作者不存在'})
        scholar = Scholar(es_id=author_id, name=result["hits"]["hits"][0]["_source"]["display_name"])
    scholar.claimed_user = user
    scholar.save()
    user.claimed_scholar = scholar
    user.save()
    data = {"name": scholar.name, "domain": data0}
    return JsonResponse({'errno': 0, 'errmsg': 'success', 'data': data})


def other_claim(request):
    if request.method != "POST":
        return JsonResponse({'errno': 1001, 'errmsg': '请求方法错误'})
    body = request.POST.copy()
    user = auth_token(body.get("token"), False)
    if user is None or user is False:
        return JsonResponse({'errno': 1002, 'errmsg': '登录错误'})
    author_id = body.get("author_id")
    claim_text = body.get("claim_text")
    claim_file = request.FILES.get("claim_file")
    if claim_text is None and claim_file is None:
        return JsonResponse({'errno': 1004, 'errmsg': '缺少认领信息'})
    if not user.claimed_scholar is None:
        return JsonResponse({'errno': 1005, 'errmsg': '用户已认领作者'})
    if Scholar.objects.filter(es_id=author_id, claimed_user_id__isnull=False).exists():
        return JsonResponse({'errno': 1006, 'errmsg': '作者已被认领'})
    scholar = None
    if Scholar.objects.filter(es_id=author_id).exists():
        scholar = Scholar.objects.get(es_id=author_id)
    else:
        search_body = {
            "query": {
                "match": {
                    "id": author_id
                }
            }
        }
        result = es_search.body_search("authors", search_body)
        if len(result["hits"]["hits"]) == 0:
            return JsonResponse({'errno': 1006, 'errmsg': '作者不存在'})
        scholar = Scholar(es_id=author_id, name=result["hits"]["hits"][0]["_source"]["display_name"])
        scholar.save()
    if claim_text is None:
        claim = Claim(scholar=scholar, claim_file=claim_file)
    elif claim_file is None:
        claim = Claim(scholar=scholar, claim_text=claim_text)
    else:
        claim = Claim(scholar=scholar, claim_text=claim_text, claim_file=claim_file)
    claim.save()
    affair = Affair(claim=claim, user=user, type=3, submit_time=datetime.datetime.now(), status=0)
    affair.save()
    return JsonResponse({'errno': 0, 'errmsg': 'success'})


def appeal_author(request):
    if request.method != "POST":
        return JsonResponse({'errno': 1001, 'errmsg': '请求方法错误'})
    body = request.POST.copy()
    user = auth_token(body.get("token"), False)
    if user is None or user is False:
        return JsonResponse({'errno': 1002, 'errmsg': '登录错误'})
    author_id = body.get("author_id")
    appeal_text = body.get("appeal_text")
    appeal_file = request.FILES.get("appeal_file")
    if appeal_text is None and appeal_file is None:
        return JsonResponse({'errno': 1004, 'errmsg': '缺少申诉信息'})
    if not Scholar.objects.filter(es_id=author_id, appealed_user_id__isnull=False).exists():
        return JsonResponse({'errno': 1006, 'errmsg': '作者未被认领'})
    scholar = Scholar.objects.get(es_id=author_id)
    if appeal_text is None:
        appeal = Appeal(scholar=scholar, appeal_file=appeal_file)
    elif appeal_file is None:
        appeal = Appeal(scholar=scholar, appeal_text=appeal_text)
    else:
        appeal = Appeal(scholar=scholar, appeal_text=appeal_text, appeal_file=appeal_file)
    appeal.save()
    affair = Affair(appeal=appeal, user=user, type=2, submit_time=datetime.datetime.now(), status=0)
    affair.save()
    return JsonResponse({'errno': 0, 'errmsg': 'success'})
