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

def claim(request):
    if request.method != "POST":
        return JsonResponse({'errno': 1001, 'errmsg': '请求方法错误'})
    body = request.POST.copy()
    user = auth_token(body.get("token"),False)
    if user is None or user is False:
        return JsonResponse({'errno': 1002, 'errmsg': '登录错误'})


