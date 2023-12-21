import base64
import json
import os.path
import time

from django.conf import settings
from django.core.signing import Signer
from django.db import models
import jwt


# Create your models here.

def encrypt(data):
    return base64.b64encode(data.encode('utf-8')).decode('utf-8')


def decrypt(data):
    return base64.b64decode(data.encode('utf-8')).decode('utf-8')


def auth_token(token, is_admin):
    salt = settings.SECRET_KEY
    try:
        payload = jwt.decode(token, salt, algorithms=['HS256'], verify=True)
        exp_time = payload['exp']
        if time.time() > exp_time:
            raise Exception('Token has expired')
    except Exception as e:
        print(e)
        return False
    if payload['type'] == 'user':
        if is_admin:
            return False
        if User.objects.filter(id=payload['id']).exists():
            return User.objects.get(id=payload['id'])
        else:
            return False
    elif payload['type'] == 'admin':
        if not is_admin:
            return False
        if Admin.objects.filter(id=payload['id']).exists():
            return Admin.objects.get(id=payload['id'])
        else:
            return False
    else:
        return False


class Scholar(models.Model):
    es_id = models.CharField(max_length=20, unique=True, null=False)
    name = models.CharField(max_length=80, null=False)
    claim_email = models.TextField(null=True)
    claimed_user_id = models.IntegerField(null=True)


class User(models.Model):
    username = models.CharField(max_length=20, unique=True, null=False)
    password = models.CharField(max_length=100, null=False)
    email = models.CharField(max_length=50, unique=True, null=False)
    claimed_scholar = models.ForeignKey(Scholar, on_delete=models.CASCADE, null=True)
    chat_history = models.CharField(max_length=100, null=False, default="")
    chat_id = models.CharField(max_length=100, null=False, default="")

    def create_token(self, timeout):
        salt = settings.SECRET_KEY
        headers = {
            "typ": "jwt",
            "alg": "HS256"
        }
        payload = {'id': self.id, 'username': self.username, 'type': 'user', 'exp': time.time() + timeout}
        token = jwt.encode(payload=payload, key=salt, algorithm="HS256", headers=headers)
        return token


class Admin(models.Model):
    username = models.CharField(max_length=20, unique=True, null=False)
    password = models.CharField(max_length=100, null=False)

    def create_token(self, timeout):
        salt = settings.SECRET_KEY
        headers = {
            "typ": "jwt",
            "alg": "HS256"
        }
        payload = {'id': self.id, 'username': self.username, 'type': 'admin', 'exp': time.time() + timeout}
        token = jwt.encode(payload=payload, key=salt, algorithm="HS256", headers=headers)
        return token


class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    paper_id = models.CharField(max_length=20, null=False)
    type = models.IntegerField(default=0)  # 0:paper 1:学者 2:机构 3:学科
    time = models.DateTimeField(auto_now=True)


class Star_folder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, null=False)
    num = models.IntegerField(default=0)


class Star(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.IntegerField(default=0)  # 0:paper 1:学者 2:机构 3:学科
    paper_id = models.CharField(max_length=20, null=False)
    folder = models.ForeignKey(Star_folder, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_time = models.DateTimeField(auto_now=True)
    paper_id = models.CharField(max_length=20, null=False)
    content = models.CharField(max_length=20, null=False)
    reply_to = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    top = models.BooleanField(default=False)


def report_file_upload_to(instance, filename):
    filename = os.path.basename(filename)
    path = 'report/' + str(instance.id) + '/'
    os.makedirs(settings.MEDIA_ROOT + path, exist_ok=True)
    path = path + filename
    while os.path.exists(settings.MEDIA_ROOT + path):
        path = path.split(".")[0] + "_1." + path.split(".")[1]
    filename = path.split('/')[-1]
    return path


#     举报
class Report(models.Model):
    paper_id = models.CharField(max_length=20, null=False)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True)
    reported_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    report_text = models.CharField(max_length=100, null=True)
    report_file = models.FileField(upload_to=report_file_upload_to, null=True)


def appeal_file_upload_to(instance, filename):
    filename = os.path.basename(filename)
    path = 'appeal/' + str(instance.id) + '/'
    os.makedirs(settings.MEDIA_ROOT + path, exist_ok=True)
    path = path + filename
    while os.path.exists(settings.MEDIA_ROOT + path):
        path = path.split(".")[0] + "_1." + path.split(".")[1]
    filename = path.split('/')[-1]
    return path


#     申诉
class Appeal(models.Model):
    appealed_scholar = models.ForeignKey(Scholar, on_delete=models.CASCADE)
    appeal_email = models.CharField(max_length=50, null=True)
    appeal_text = models.CharField(max_length=100, null=True)
    appeal_file = models.FileField(upload_to=appeal_file_upload_to, null=True)


def claim_file_upload_to(instance, filename):
    filename = os.path.basename(filename)
    path = 'claim/' + str(instance.id) + '/'
    os.makedirs(settings.MEDIA_ROOT + path, exist_ok=True)
    path = path + filename
    while os.path.exists(settings.MEDIA_ROOT + path):
        path = path.split(".")[0] + "_1." + path.split(".")[1]
    filename = path.split('/')[-1]
    return path


#     认证
class Claim(models.Model):
    claimed_scholar = models.ForeignKey(Scholar, on_delete=models.CASCADE)
    claim_email = models.CharField(max_length=50, null=True)
    claim_text = models.CharField(max_length=100, null=True)
    claim_file = models.FileField(upload_to=claim_file_upload_to, null=True)


class Affair(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.IntegerField(default=0)
    report = models.ForeignKey(Report, on_delete=models.CASCADE, null=True)
    appeal = models.ForeignKey(Appeal, on_delete=models.CASCADE, null=True)
    claim = models.ForeignKey(Claim, on_delete=models.CASCADE, null=True)
    submit_time = models.DateTimeField(auto_now_add=True)
    handle_time = models.DateTimeField(auto_now=True)
    handle_reason = models.CharField(max_length=100, null=True)
    status = models.IntegerField(default=0)


class Paper_display(models.Model):
    es_id = models.CharField(max_length=20, unique=True, null=False)
    author_id = models.CharField(max_length=20, null=False)


class Paper_delete(models.Model):
    es_id = models.CharField(max_length=20, unique=True, null=False)
