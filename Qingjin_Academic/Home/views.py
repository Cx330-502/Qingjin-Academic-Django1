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


def encrypt(data):
    return base64.b64encode(data.encode('utf-8')).decode('utf-8')


def decrypt(data):
    return base64.b64decode(data.encode('utf-8')).decode('utf-8')


def md5_encrypt(plaintext):
    md5 = hashlib.md5()
    md5.update(plaintext.encode('utf-8'))
    ciphertext = md5.hexdigest()
    return ciphertext


def captcha(request):
    if request.method != "POST":
        return JsonResponse({'errno': 1001, 'errmsg': '请求方法错误'})
    body = json.loads(request.body)
    receiver_email = body.get("email")
    try:
        validate_email(receiver_email)
    except ValidationError:
        return JsonResponse({'errno': 1002, 'errmsg': '邮箱不符合规范'})
    verification = captchaClass.SendEmail(data=captchaClass.data,
                                          receiver=receiver_email).send_email()
    verification = encrypt(verification)
    data = {"verification": verification}
    return JsonResponse({'errno': 0, 'errmsg': '验证码发送成功', 'data': data})


def user_register(request):
    if request.method != "POST":
        return JsonResponse({'errno': 1001, 'errmsg': '请求方法错误'})
    body = json.loads(request.body)
    username = body.get("username")
    password = body.get("password")
    email = body.get("email")
    if username is None:
        return JsonResponse({'errno': 1002, 'errmsg': '用户名不能为空'})
    if password is None:
        return JsonResponse({'errno': 1003, 'errmsg': '密码不能为空'})
    if email is None:
        return JsonResponse({'errno': 1004, 'errmsg': '邮箱不能为空'})
    if not re.match(r"^[a-zA-Z0-9\u4e00-\u9fa5_-]{2,16}$", username):
        return JsonResponse({'errno': 1005, 'errmsg': '用户名不符合规范'})
    if User.objects.filter(username=username).exists():
        return JsonResponse({'errno': 1007, 'errmsg': '用户名已存在'})
    if User.objects.filter(email=email).exists():
        return JsonResponse({'errno': 1008, 'errmsg': '邮箱已存在'})
    password = md5_encrypt(password)
    user = User(username=username, password=password, email=email)
    user.save()
    return JsonResponse({'errno': 0, 'errmsg': '注册成功', 'data': {
        'user_id': user.id,
        'username': user.username,
        'email': user.email
    }})


def user_login(request):
    if request.method != "POST":
        return JsonResponse({'errno': 1001, 'errmsg': '请求方法错误'})
    body = json.loads(request.body)
    username = body.get("username")
    password = body.get("password")
    is_admin = False
    if User.objects.filter(username=username).exists():
        user = User.objects.get(username=username)
    elif User.objects.filter(email=username).exists():
        user = User.objects.get(email=username)
    elif Admin.objects.filter(username=username).exists():
        user = Admin.objects.get(username=username)
        is_admin = True
    else:
        return JsonResponse({'errno': 1002, 'errmsg': '用户名或邮箱不存在'})
    if user.password == md5_encrypt(password):
        token = user.create_token(3600 * 24)
        data = {'token': token,
                'user_id': user.id,
                'username': user.username,
                'email': user.email,
                'is_admin': is_admin
                }
        return JsonResponse(
            {'errno': 0, 'errmsg': '登录成功', 'data': data})
    return JsonResponse({'errno': 1003, 'errmsg': '密码错误'})


def hot_paper(request):
    if request.method != "POST":
        return JsonResponse({'errno': 1001, 'errmsg': '请求方法错误'})
    body = json.loads(request.body)
    search_body = {
        "query": {
            "match_all": {}  # 可以根据需要修改查询条件
        },
        "sort": [
            {"cited_count": {"order": "desc"}}  # 根据引用量字段降序排序
        ],
        "size": 10  # 获取前十条结果
    }
    result = es_search.body_search(index="works", body=search_body)
    result = es_handle.hot_paper_handle(result)
    return JsonResponse({'errno': 0, 'errmsg': '查询成功', 'data': result})


def hot_institution(request):
    if request.method != "POST":
        return JsonResponse({'errno': 1001, 'errmsg': '请求方法错误'})
    body = json.loads(request.body)
    search_body = {
        "query": {
            "match_all": {}  # 可以根据需要修改查询条件
        },
        "sort": [
            {"summary_stats.h_index": {"order": "desc"}}  # 根据活跃度字段降序排序
        ],
        "size": 10  # 获取前十条结果
    }
    result = es_search.body_search(index="institutions", body=search_body)
    result = es_handle.hot_institution_handle(result)
    return JsonResponse({'errno': 0, 'errmsg': '查询成功', 'data': result})


def get_history(request):
    if request.method != "POST":
        return JsonResponse({'errno': 1001, 'errmsg': '请求方法错误'})
    body = json.loads(request.body)
    user = auth_token(body.get("token"), False)
    if user is None or user is False:
        return JsonResponse({'errno': 1002, 'errmsg': '登录错误'})
    history = History.objects.filter(user=user).all()
    result_ids = []
    for h in history:
        result_ids.append(h.paper_id)
    search_body = {
        "query": {
            "terms": {
                "_id": result_ids
            }
        }
    }
    result = es_search.body_search('works', search_body)
    result = es_handle.hot_paper_handle(result)
    return JsonResponse({'errno': 0, 'errmsg': '查询成功', 'data': result})


def clear_history(request):
    if request.method != "POST":
        return JsonResponse({'errno': 1001, 'errmsg': '请求方法错误'})
    body = json.loads(request.body)
    user = auth_token(body.get("token"), False)
    if user is None or user is False:
        return JsonResponse({'errno': 1002, 'errmsg': '登录错误'})
    history = History.objects.filter(user=user).all()
    for h in history:
        h.delete()
    return JsonResponse({'errno': 0, 'errmsg': '清除成功'})


def get_stars(request):
    if request.method != "POST":
        return JsonResponse({'errno': 1001, 'errmsg': '请求方法错误'})
    body = json.loads(request.body)
    user = auth_token(body.get("token"), False)
    if user is None or user is False:
        return JsonResponse({'errno': 1002, 'errmsg': '登录错误'})
    star_folders = Star_folder.objects.filter(user=user).all()
    result = {}
    oppo_dict = {}
    star_list = []
    for folder in star_folders:
        result[folder.name] = []
        stars = Star.objects.filter(folder=folder).all()
        for star in stars:
            star_list.append(star.paper_id)
            oppo_dict[star.paper_id] = folder.name
    search_body = {
        "query": {
            "terms": {
                "_id": star_list
            }
        }
    }
    result0 = es_search.body_search('works', search_body)
    result0 = es_handle.hot_paper_handle(result0)
    for result1 in result0:
        result[oppo_dict[result1['id']]].append(result1)
    return JsonResponse({'errno': 0, 'errmsg': '查询成功', 'data': result})


def unstar(request):
    if request.method != "POST":
        return JsonResponse({'errno': 1001, 'errmsg': '请求方法错误'})
    body = json.loads(request.body)
    user = auth_token(body.get("token"), False)
    if user is None or user is False:
        return JsonResponse({'errno': 1002, 'errmsg': '登录错误'})
    paper_id = body.get("paper_id")
    if paper_id is None:
        return JsonResponse({'errno': 1003, 'errmsg': 'paper_id不能为空'})
    star = Star.objects.filter(user=user, paper_id=paper_id).first()
    folder = star.folder
    folder.num -= 1
    star.delete()
    return JsonResponse({'errno': 0, 'errmsg': '取消收藏成功'})


def create_folder(request):
    if request.method != "POST":
        return JsonResponse({'errno': 1001, 'errmsg': '请求方法错误'})
    body = json.loads(request.body)
    user = auth_token(body.get("token"), False)
    if user is None or user is False:
        return JsonResponse({'errno': 1002, 'errmsg': '登录错误'})
    folder_name = body.get("folder_name")
    if folder_name is None:
        return JsonResponse({'errno': 1003, 'errmsg': 'folder_name不能为空'})
    if Star_folder.objects.filter(user=user, name=folder_name).exists():
        return JsonResponse({'errno': 1004, 'errmsg': '收藏夹已存在'})
    folder = Star_folder(user=user, name=folder_name, num=0)
    folder.save()
    return JsonResponse({'errno': 0, 'errmsg': '新建文件夹成功'})


def move_star(request):
    if request.method != "POST":
        return JsonResponse({'errno': 1001, 'errmsg': '请求方法错误'})
    body = json.loads(request.body)
    user = auth_token(body.get("token"), False)
    if user is None or user is False:
        return JsonResponse({'errno': 1002, 'errmsg': '登录错误'})
    paper_id = body.get("paper_id")
    folder_name = body.get("folder_name")
    if paper_id is None:
        return JsonResponse({'errno': 1003, 'errmsg': 'paper_id不能为空'})
    if folder_name is None:
        return JsonResponse({'errno': 1004, 'errmsg': 'folder_name不能为空'})
    if not Star_folder.objects.filter(user=user, name=folder_name).exists():
        return JsonResponse({'errno': 1005, 'errmsg': '收藏夹不存在'})
    folder = Star_folder.objects.get(user=user, name=folder_name)
    star = Star.objects.filter(user=user, paper_id=paper_id).first()
    star.folder.num -= 1
    star.folder = folder
    star.save()
    return JsonResponse({'errno': 0, 'errmsg': '移动成功'})

def delete_folder(request):
    if request.method != "POST":
        return JsonResponse({'errno': 1001, 'errmsg': '请求方法错误'})
    body = json.loads(request.body)
    user = auth_token(body.get("token"), False)
    if user is None or user is False:
        return JsonResponse({'errno': 1002, 'errmsg': '登录错误'})
    folder_name = body.get("folder_name")
    if folder_name is None or not Star_folder.objects.filter(user=user, name=folder_name).exists():
        return JsonResponse({'errno': 1004, 'errmsg': 'folder_name不能为空'})
    folder = Star_folder.objects.get(user=user, name=folder_name)
    folder.delete()
    return JsonResponse({'errno': 0, 'errmsg': '删除成功'})
