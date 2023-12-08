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
    result_ids_0 = []
    result_ids_1 = []
    result_ids_2 = []
    result_ids_3 = []
    history_ids_0 = {}
    history_ids_1 = {}
    history_ids_2 = {}
    history_ids_3 = {}
    for h in history:
        if h.type == 0:
            result_ids_0.append(h.paper_id)
            history_ids_0[h.paper_id] = {'history_id': h.id, 'time': h.time.strftime("%Y-%m-%d %H:%M:%S"), 'type': 0}
        elif h.type == 1:
            result_ids_1.append(h.paper_id)
            history_ids_1[h.paper_id] = {'history_id': h.id, 'time': h.time.strftime("%Y-%m-%d %H:%M:%S"), 'type': 1}
        elif h.type == 2:
            result_ids_2.append(h.paper_id)
            history_ids_2[h.paper_id] = {'history_id': h.id, 'time': h.time.strftime("%Y-%m-%d %H:%M:%S"), 'type': 2}
        elif h.type == 3:
            result_ids_3.append(h.paper_id)
            history_ids_3[h.paper_id] = {'history_id': h.id, 'time': h.time.strftime("%Y-%m-%d %H:%M:%S"), 'type': 3}
    search_body_0 = {
        "query": {
            "terms": {
                "_id": result_ids_0
            }
        }
    }
    result_0 = es_search.body_search('works', search_body_0)
    result_0 = es_handle.hot_paper_handle(result_0)
    search_body_1 = {
        "query": {
            "terms": {
                "_id": result_ids_1
            }
        }
    }
    result_1 = es_search.body_search('authors', search_body_1)
    result_1 = es_handle.author_handle(result_1)
    search_body_2 = {
        "query": {
            "terms": {
                "_id": result_ids_2
            }
        }
    }
    result_2 = es_search.body_search('institutions', search_body_2)
    result_2 = es_handle.hot_institution_handle(result_2)
    search_body_3 = {
        "query": {
            "terms": {
                "_id": result_ids_3
            }
        }
    }
    result_3 = es_search.body_search('concepts', search_body_3)
    result_3 = es_handle.concept_handle(result_3)
    result = []
    for result0 in result_0:
        temp = history_ids_0[result0['id']]
        temp['data'] = result0
        result.append(temp)
    for result1 in result_1:
        temp = history_ids_1[result1['id']]
        temp['data'] = result1
        result.append(temp)
    for result2 in result_2:
        temp = history_ids_2[result2['id']]
        temp['data'] = result2
        result.append(temp)
    for result3 in result_3:
        temp = history_ids_3[result3['id']]
        temp['data'] = result3
        result.append(temp)
    result.sort(key=lambda x: x['time'], reverse=True)
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


def delete_history(request):
    if request.method != "POST":
        return JsonResponse({'errno': 1001, 'errmsg': '请求方法错误'})
    body = json.loads(request.body)
    user = auth_token(body.get("token"), False)
    if user is None or user is False:
        return JsonResponse({'errno': 1002, 'errmsg': '登录错误'})
    history_id = body.get("history_id")
    if history_id is None or not History.objects.filter(id=history_id).exists():
        return JsonResponse({'errno': 1003, 'errmsg': 'history_id不能为空'})
    history = History.objects.get(id=history_id)
    history.delete()
    return JsonResponse({'errno': 0, 'errmsg': '删除成功'})


def get_stars(request):
    if request.method != "POST":
        return JsonResponse({'errno': 1001, 'errmsg': '请求方法错误'})
    body = json.loads(request.body)
    user = auth_token(body.get("token"), False)
    if user is None or user is False:
        return JsonResponse({'errno': 1002, 'errmsg': '登录错误'})
    star_folders = Star_folder.objects.filter(user=user).all()
    result = {}
    star_list_0 = []
    star_list_1 = []
    star_list_2 = []
    star_list_3 = []
    oppo_dict_0 = {}
    oppo_dict_1 = {}
    oppo_dict_2 = {}
    oppo_dict_3 = {}
    for folder in star_folders:
        result[folder.name] = {'name': folder.name, 'list': [], 'folder_id': folder.id, 'num': folder.num}
        stars = Star.objects.filter(folder=folder).all()
        for star in stars:
            if star.type == 0:
                star_list_0.append(star.paper_id)
                oppo_dict_0[star.paper_id] = {'star_id': star.id, 'type': 0,
                                              'time': star.time.strftime("%Y-%m-%d %H:%M:%S"),
                                              'folder_id': folder.id, 'folder_name': folder.name}
            elif star.type == 1:
                star_list_1.append(star.paper_id)
                oppo_dict_1[star.paper_id] = {'star_id': star.id, 'type': 1,
                                              'time': star.time.strftime("%Y-%m-%d %H:%M:%S"),
                                              'folder_id': folder.id, 'folder_name': folder.name}
            elif star.type == 2:
                star_list_2.append(star.paper_id)
                oppo_dict_2[star.paper_id] = {'star_id': star.id, 'type': 2,
                                              'time': star.time.strftime("%Y-%m-%d %H:%M:%S"),
                                              'folder_id': folder.id, 'folder_name': folder.name}
            elif star.type == 3:
                star_list_3.append(star.paper_id)
                oppo_dict_3[star.paper_id] = {'star_id': star.id, 'type': 3,
                                              'time': star.time.strftime("%Y-%m-%d %H:%M:%S"),
                                              'folder_id': folder.id, 'folder_name': folder.name}
    search_body_0 = {
        "query": {
            "terms": {
                "_id": star_list_0
            }
        }
    }
    result0 = es_search.body_search('works', search_body_0)
    result0 = es_handle.hot_paper_handle(result0)
    search_body_1 = {
        "query": {
            "terms": {
                "_id": star_list_1
            }
        }
    }
    result1 = es_search.body_search('authors', search_body_1)
    result1 = es_handle.author_handle(result1)
    search_body_2 = {
        "query": {
            "terms": {
                "_id": star_list_2
            }
        }
    }
    result2 = es_search.body_search('institutions', search_body_2)
    result2 = es_handle.hot_institution_handle(result2)
    search_body_3 = {
        "query": {
            "terms": {
                "_id": star_list_3
            }
        }
    }
    result3 = es_search.body_search('concepts', search_body_3)
    result3 = es_handle.concept_handle(result3)
    for result_0 in result0:
        temp = oppo_dict_0[result_0['id']]
        temp['data'] = result_0
        result[temp['folder_name']]['list'].append(temp)
    for result_1 in result1:
        temp = oppo_dict_1[result_1['id']]
        temp['data'] = result_1
        result[temp['folder_name']]['list'].append(temp)
    for result_2 in result2:
        temp = oppo_dict_2[result_2['id']]
        temp['data'] = result_2
        result[temp['folder_name']]['list'].append(temp)
    for result_3 in result3:
        temp = oppo_dict_3[result_3['id']]
        temp['data'] = result_3
        result[temp['folder_name']]['list'].append(temp)
    result000 = []
    for folder in result.keys():
        result[folder]['list'].sort(key=lambda x: x['time'], reverse=True)
        result000.append(result[folder])
    result000.sort(key=lambda x: x['id'], reverse=True)
    return JsonResponse({'errno': 0, 'errmsg': '查询成功', 'data': result000})


def get_folders(request):
    if request.method != "POST":
        return JsonResponse({'errno': 1001, 'errmsg': '请求方法错误'})
    body = json.loads(request.body)
    user = auth_token(body.get("token"), False)
    if user is None or user is False:
        return JsonResponse({'errno': 1002, 'errmsg': '登录错误'})
    star_folders = Star_folder.objects.filter(user=user).all()
    result = []
    for folder in star_folders:
        result.append({'folder_id': folder.id, 'folder_name': folder.name, 'num': folder.num})
    return JsonResponse({'errno': 0, 'errmsg': '查询成功', 'data': result})


def unstar(request):
    if request.method != "POST":
        return JsonResponse({'errno': 1001, 'errmsg': '请求方法错误'})
    body = json.loads(request.body)
    user = auth_token(body.get("token"), False)
    if user is None or user is False:
        return JsonResponse({'errno': 1002, 'errmsg': '登录错误'})
    star_id = body.get("star_id")
    if star_id is None or not Star.objects.filter(id=star_id).exists():
        return JsonResponse({'errno': 1003, 'errmsg': 'star_id不能为空'})
    star = Star.objects.filter(id=star_id).first()
    folder = star.folder
    folder.num -= 1
    star.delete()
    folder.save()
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
    data = {
        'folder_id': folder.id,
        'folder_name': folder.name,
        'num': folder.num
    }
    return JsonResponse({'errno': 0, 'errmsg': '新建文件夹成功', 'data': data})


def move_star(request):
    if request.method != "POST":
        return JsonResponse({'errno': 1001, 'errmsg': '请求方法错误'})
    body = json.loads(request.body)
    user = auth_token(body.get("token"), False)
    if user is None or user is False:
        return JsonResponse({'errno': 1002, 'errmsg': '登录错误'})
    paper_id = body.get("paper_id")
    folder_id = body.get("folder_id")
    if paper_id is None:
        return JsonResponse({'errno': 1003, 'errmsg': 'paper_id不能为空'})
    if folder_id is None:
        return JsonResponse({'errno': 1004, 'errmsg': 'folder_id不能为空'})
    if not Star_folder.objects.filter(id=folder_id).exists():
        return JsonResponse({'errno': 1005, 'errmsg': '收藏夹不存在'})
    folder = Star_folder.objects.get(id=folder_id)
    star = Star.objects.filter(user=user, paper_id=paper_id).first()
    star.folder.num -= 1
    star.folder.save()
    star.folder = folder
    folder.num += 1
    star.save()
    folder.save()
    return JsonResponse({'errno': 0, 'errmsg': '移动成功'})


def delete_folder(request):
    if request.method != "POST":
        return JsonResponse({'errno': 1001, 'errmsg': '请求方法错误'})
    body = json.loads(request.body)
    user = auth_token(body.get("token"), False)
    if user is None or user is False:
        return JsonResponse({'errno': 1002, 'errmsg': '登录错误'})
    folder_id = body.get("folder_id")
    if folder_id is None or not Star_folder.objects.filter(id=folder_id).exists():
        return JsonResponse({'errno': 1003, 'errmsg': 'folder_id不能为空'})
    folder = Star_folder.objects.get(id=folder_id)
    folder.delete()
    return JsonResponse({'errno': 0, 'errmsg': '删除成功'})


def add_history(request):
    if request.method != "POST":
        return JsonResponse({'errno': 1001, 'errmsg': '请求方法错误'})
    body = json.loads(request.body)
    user = auth_token(body.get("token"), False)
    if user is None or user is False:
        return JsonResponse({'errno': 1002, 'errmsg': '登录错误'})
    paper_id = body.get("paper_id")
    type = body.get("type")
    if paper_id is None:
        return JsonResponse({'errno': 1003, 'errmsg': 'paper_id不能为空'})
    if type is None:
        return JsonResponse({'errno': 1004, 'errmsg': 'type不能为空'})
    if not History.objects.filter(user=user, paper_id=paper_id, type=type).exists():
        history = History(user=user, paper_id=paper_id, type=type)
        history.save()
    return JsonResponse({'errno': 0, 'errmsg': '添加成功'})


def star(request):
    if request.method != "POST":
        return JsonResponse({'errno': 1001, 'errmsg': '请求方法错误'})
    body = json.loads(request.body)

    user = auth_token(body.get("token"), False)
    if user is None or user is False:
        return JsonResponse({'errno': 1002, 'errmsg': '登录错误'})

    paper_id = body.get("paper_id")
    type = body.get("type")
    folder_id = body.get("folder_id")
    if paper_id is None:
        return JsonResponse({'errno': 1003, 'errmsg': 'paper_id不能为空'})
    if type is None:
        return JsonResponse({'errno': 1004, 'errmsg': 'type不能为空'})
    if folder_id is None or not Star_folder.objects.filter(id=folder_id).exists():
        return JsonResponse({'errno': 1005, 'errmsg': 'folder_id不能为空'})
    if Star.objects.filter(user=user, paper_id=paper_id).exists():
        return JsonResponse({'errno': 1006, 'errmsg': '已收藏'})
    folder = Star_folder.objects.get(id=folder_id)
    folder.num += 1
    folder.save()
    star0 = Star(user=user, paper_id=paper_id, type=type, folder=folder)
    star0.save()
    return JsonResponse({'errno': 0, 'errmsg': '收藏成功', 'data': {'star_id': star0.id}})
