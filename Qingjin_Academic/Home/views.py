import random
import base64
import re
import Home.extra_codes.captcha as captchaClass

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
    if not re.match(r"^[a-zA-Z0-9_-]{6,16}$", password):
        return JsonResponse({'errno': 1006, 'errmsg': '密码不符合规范'})
    if User.objects.filter(username=username).exists():
        return JsonResponse({'errno': 1007, 'errmsg': '用户名已存在'})
    if User.objects.filter(email=email).exists():
        return JsonResponse({'errno': 1008, 'errmsg': '邮箱已存在'})
    user = User(username=username, password=password, email=email)
    user.save()
    if user.avatar.name == "" or user.avatar.name is None:
        ran_num = random.randint(1, 6)
        path = settings.MEDIA_ROOT + '/avatar/' + 'default/' + str(ran_num) + '.jpg'
        with open(path, 'rb') as f:
            user.avatar = File(f)
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
    if User.objects.filter(username=username).exists():
        user = User.objects.get(username=username)
    elif User.objects.filter(email=username).exists():
        user = User.objects.get(email=username)
    else:
        return JsonResponse({'errno': 1002, 'errmsg': '用户名或邮箱不存在'})
    if user.password == password:
        token = user.create_token(3600 * 24)
        avatar_url = None
        if user.avatar and user.avatar.name:
            avatar_url = settings.BACKEND_URL + user.avatar.url
        user.login_times = user.login_times + 1
        user.save()
        data = {'token': token,
                'user_id': user.id,
                'username': user.username,
                'email': user.email}
        return JsonResponse(
            {'errno': 0, 'errmsg': '登录成功', 'data': data})
    return JsonResponse({'errno': 1003, 'errmsg': '密码错误'})
