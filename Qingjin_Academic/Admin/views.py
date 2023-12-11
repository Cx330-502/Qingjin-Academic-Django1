import datetime
import random
import base64
import re
import Admin.extra_codes.notice as noticeClass
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
def md5_encrypt(plaintext):
    md5 = hashlib.md5()
    md5.update(plaintext.encode('utf-8'))
    ciphertext = md5.hexdigest()
    return ciphertext

def get_affairs(request):
    if request.method != "POST":
        return JsonResponse({'errno': 1001, 'errmsg': '请求方法错误'})
    body = json.loads(request.body)
    user = auth_token(body.get("token"), True)
    if user is None or user is False:
        return JsonResponse({'errno': 1002, 'errmsg': '登录错误'})
    affairs = Affair.objects.filter(status=0)
    return_data = {
        "appeal": [],
        "claim": [],
        "report": [],
    }
    for affair in affairs:
        if affair.type == 1:
            paper_id = affair.report.paper_id
            search_body = {
                "query": {
                    "match": {
                        "id": paper_id
                    }
                }
            }
            result = es_search.body_search("works", search_body)
            if len(result["hits"]["hits"]) == 0:
                return JsonResponse({'errno': 1003, 'errmsg': '论文不存在'})
            paper = result["hits"]["hits"][0]["_source"]["title"]
            data = {
                "affair_id": affair.id,
                "user_id": affair.user.id,
                "username": affair.user.username,
                "paper_id": affair.report.paper_id,
                "paper_title": paper,
                "submit_time": affair.submit_time.strftime("%Y-%m-%d %H:%M:%S"),
                "comment_id": -1,
                "comment_content": "",
                "comment_user": "",
                "comment_user_id": -1,
                "comment_time": "",
                "report_text": "",
                "report_file": ""
            }
            if affair.report.comment is not None:
                data["comment_id"] = affair.report.comment.id
                data["comment_content"] = affair.report.comment.content
                data["comment_user"] = affair.report.comment.user.username
                data["comment_user_id"] = affair.report.comment.user.id
                data["comment_time"] = affair.report.comment.comment_time.strftime("%Y-%m-%d %H:%M:%S")
            if affair.report.report_text is not None:
                data["report_text"] = affair.report.report_text
            if affair.report.report_file is not None and affair.report.report_file.name != "":
                data["report_file"] = settings.BACKEND_URL + affair.report.report_file.url
            return_data["report"].append(data)
        if affair.type == 2:
            scholar_id = affair.appeal.appealed_scholar.es_id
            scholar_name = affair.appeal.appealed_scholar.name
            data = {
                "affair_id": affair.id,
                "user_id": affair.user.id,
                "username": affair.user.username,
                "scholar_id": scholar_id,
                "scholar_name": scholar_name,
                "submit_time": affair.submit_time.strftime("%Y-%m-%d %H:%M:%S"),
                "appeal_text": "",
                "appeal_file": "",
                "appeal_email": "",
                "appeal_type": 0,
                "appeal_email_common": False
            }
            if affair.appeal.appeal_text is not None:
                data["appeal_text"] = affair.appeal.appeal_text
            if affair.appeal.appeal_file is not None and affair.appeal.appeal_file.name != "":
                data["appeal_file"] = settings.BACKEND_URL + affair.appeal.appeal_file.url
            if affair.appeal.appeal_email is not None:
                data["appeal_email"] = affair.appeal.appeal_email
                data["appeal_type"] = 1
                temp_email_domain = affair.appeal.appeal_email.split("@")[1].split(".")
                temp = "./Author/domains/common/"
                j = len(temp_email_domain)
                while j > 0:
                    temp += temp_email_domain[j - 1] + "/"
                    j -= 1
                temp += '.txt'
                if os.path.exists(temp):
                    data['appeal_email_common'] = True
            return_data["appeal"].append(data)
        if affair.type == 3:
            scholar_id = affair.claim.claimed_scholar.es_id
            scholar_name = affair.claim.claimed_scholar.name
            data = {
                "affair_id": affair.id,
                "user_id": affair.user.id,
                "username": affair.user.username,
                "scholar_id": scholar_id,
                "scholar_name": scholar_name,
                "submit_time": affair.submit_time.strftime("%Y-%m-%d %H:%M:%S"),
                "claim_text": "",
                "claim_file": "",
                "claim_email": affair.claim.claim_email,
                "claim_email_common": False
            }
            if affair.claim.claim_text is not None:
                data["claim_text"] = affair.claim.claim_text
            if affair.claim.claim_file is not None and affair.claim.claim_file.name != "":
                data["claim_file"] = settings.BACKEND_URL + affair.claim.claim_file.url
            temp_email_domain = affair.claim.claim_email.split("@")[1].split(".")
            temp = "./Author/domains/common/"
            j = len(temp_email_domain)
            while j > 0:
                temp += temp_email_domain[j - 1] + "/"
                j -= 1
            temp += '.txt'
            if os.path.exists(temp):
                data['claim_email_common'] = True
            return_data["claim"].append(data)
    for key in return_data.keys():
        return_data[key].sort(key=lambda x: x["submit_time"], reverse=True)
    return JsonResponse({'errno': 0, 'errmsg': '获取事务成功', 'data': return_data})


def get_detailed_report(request):
    if request.method != "POST":
        return JsonResponse({'errno': 1001, 'errmsg': '请求方法错误'})
    body = json.loads(request.body)
    user = auth_token(body.get("token"), True)
    if user is None or user is False:
        return JsonResponse({'errno': 1002, 'errmsg': '登录错误'})
    affair_id = body.get("affair_id")
    if affair_id is None:
        return JsonResponse({'errno': 1003, 'errmsg': '缺少事务id'})
    if not Affair.objects.filter(id=affair_id).exists():
        return JsonResponse({'errno': 1004, 'errmsg': '事务不存在'})
    affair = Affair.objects.get(id=affair_id)
    if affair.type != 1:
        return JsonResponse({'errno': 1005, 'errmsg': '事务类型错误'})
    paper_id = affair.report.paper_id
    search_body = {
        "query": {
            "match": {
                "id": paper_id
            }
        }
    }
    result = es_search.body_search("works", search_body)
    if len(result["hits"]["hits"]) == 0:
        return JsonResponse({'errno': 1006, 'errmsg': '论文不存在'})
    result = es_handle.paper_handle2(result)
    return JsonResponse({'errno': 0, 'errmsg': '获取事务成功', 'data': result})


def get_detailed_appeal(request):
    if request.method != "POST":
        return JsonResponse({'errno': 1001, 'errmsg': '请求方法错误'})
    body = json.loads(request.body)
    user = auth_token(body.get("token"), True)
    if user is None or user is False:
        return JsonResponse({'errno': 1002, 'errmsg': '登录错误'})
    affair_id = body.get("affair_id")
    if affair_id is None:
        return JsonResponse({'errno': 1003, 'errmsg': '缺少事务id'})
    if not Affair.objects.filter(id=affair_id).exists():
        return JsonResponse({'errno': 1004, 'errmsg': '事务不存在'})
    affair = Affair.objects.get(id=affair_id)
    if affair.type != 2:
        return JsonResponse({'errno': 1005, 'errmsg': '事务类型错误'})
    scholar_id = affair.appeal.appealed_scholar.es_id
    search_body = {
        "query": {
            "match": {
                "id": scholar_id
            }
        }
    }
    result = es_search.body_search("authors", search_body)
    if len(result["hits"]["hits"]) == 0:
        return JsonResponse({'errno': 1006, 'errmsg': '学者不存在'})
    result = es_handle.author_handle2(result)
    return JsonResponse({'errno': 0, 'errmsg': '获取事务成功', 'data': result})


def get_detailed_claim(request):
    if request.method != "POST":
        return JsonResponse({'errno': 1001, 'errmsg': '请求方法错误'})
    body = json.loads(request.body)
    user = auth_token(body.get("token"), True)
    if user is None or user is False:
        return JsonResponse({'errno': 1002, 'errmsg': '登录错误'})
    affair_id = body.get("affair_id")
    if affair_id is None:
        return JsonResponse({'errno': 1003, 'errmsg': '缺少事务id'})
    if not Affair.objects.filter(id=affair_id).exists():
        return JsonResponse({'errno': 1004, 'errmsg': '事务不存在'})
    affair = Affair.objects.get(id=affair_id)
    if affair.type != 3:
        return JsonResponse({'errno': 1005, 'errmsg': '事务类型错误'})
    scholar_id = affair.claim.claimed_scholar.es_id
    search_body = {
        "query": {
            "match": {
                "id": scholar_id
            }
        }
    }
    result = es_search.body_search("authors", search_body)
    if len(result["hits"]["hits"]) == 0:
        return JsonResponse({'errno': 1006, 'errmsg': '学者不存在'})
    result = es_handle.author_handle2(result)
    return JsonResponse({'errno': 0, 'errmsg': '获取事务成功', 'data': result})


def handle_report(request):
    if request.method != "POST":
        return JsonResponse({'errno': 1001, 'errmsg': '请求方法错误'})
    body = json.loads(request.body)
    user = auth_token(body.get("token"), True)
    if user is None or user is False:
        return JsonResponse({'errno': 1002, 'errmsg': '登录错误'})
    affair_id = body.get("affair_id")
    if affair_id is None or not Affair.objects.filter(id=affair_id).exists():
        return JsonResponse({'errno': 1003, 'errmsg': '事务不存在'})
    affair = Affair.objects.get(id=affair_id)
    if affair.type != 1:
        return JsonResponse({'errno': 1007, 'errmsg': '事务类型错误'})
    handle_reason = body.get("handle_reason")
    if handle_reason is None:
        return JsonResponse({'errno': 1004, 'errmsg': '缺少处理理由'})
    decision = body.get("decision")
    # 0 不处理 1 删除评论 2删除论文
    if decision is None:
        return JsonResponse({'errno': 1005, 'errmsg': '缺少处理决定'})
    user = affair.user
    if decision == 0:
        noticeClass.SendEmail(data=noticeClass.data,
                              receiver=user.email,
                              time=affair.submit_time.strftime("%Y-%m-%d %H:%M:%S"),
                              affair_name="举报",
                              username=user.username,
                              decision="不处理",
                              reason=handle_reason).send_email(1)
        report = affair.report
        report.delete()
    elif decision == 1:
        if affair.report.comment is None:
            return JsonResponse({'errno': 1006, 'errmsg': '评论不存在'})
        noticeClass.SendEmail(data=noticeClass.data,
                              receiver=user.email,
                              time=affair.submit_time.strftime("%Y-%m-%d %H:%M:%S"),
                              affair_name="举报",
                              username=user.username,
                              decision="删除评论",
                              reason=handle_reason).send_email(1)
        report = affair.report
        comment = report.comment
        comment.delete()
    elif decision == 2:
        noticeClass.SendEmail(data=noticeClass.data,
                              receiver=user.email,
                              time=affair.submit_time.strftime("%Y-%m-%d %H:%M:%S"),
                              affair_name="举报",
                              username=user.username,
                              decision="删除论文",
                              reason=handle_reason).send_email(1)
        affair.status = -1
        affair.save()
    return JsonResponse({'errno': 0, 'errmsg': '处理成功'})


def handle_claim(request):
    if request.method != "POST":
        return JsonResponse({'errno': 1001, 'errmsg': '请求方法错误'})
    body = json.loads(request.body)
    user = auth_token(body.get("token"), True)
    if user is None or user is False:
        return JsonResponse({'errno': 1002, 'errmsg': '登录错误'})
    affair_id = body.get("affair_id")
    if affair_id is None or not Affair.objects.filter(id=affair_id).exists():
        return JsonResponse({'errno': 1003, 'errmsg': '事务不存在'})
    affair = Affair.objects.get(id=affair_id)
    if affair.type != 3:
        return JsonResponse({'errno': 1006, 'errmsg': '事务类型错误'})
    user = affair.user
    handle_reason = body.get("handle_reason")
    if handle_reason is None:
        return JsonResponse({'errno': 1004, 'errmsg': '缺少处理理由'})
    decision = body.get("decision")
    # 0 不通过 1 通过
    if decision is None:
        return JsonResponse({'errno': 1005, 'errmsg': '缺少处理决定'})
    claim_email_special = body.get("claim_email_special")
    # 0 不知道 1 是机构特有邮箱 -1 是普通邮箱
    if claim_email_special is None:
        claim_email_special = 0
    if decision == 0:
        noticeClass.SendEmail(data=noticeClass.data,
                              receiver=user.email,
                              time=affair.submit_time.strftime("%Y-%m-%d %H:%M:%S"),
                              affair_name="认领学者身份",
                              username=user.username,
                              decision="不通过",
                              reason=handle_reason).send_email(1)
        affair.claim.delete()
    elif decision == 1:
        if affair.claim.claimed_scholar.claimed_user_id is not None:
            return JsonResponse({'errno': 1006, 'errmsg': '该学者已被认领'})
        noticeClass.SendEmail(data=noticeClass.data,
                              receiver=user.email,
                              time=affair.submit_time.strftime("%Y-%m-%d %H:%M:%S"),
                              affair_name="认领学者身份",
                              username=user.username,
                              decision="通过",
                              reason=handle_reason).send_email(1)
        claim = affair.claim
        claim.claimed_scholar.claimed_user_id = user.id
        if claim.claimed_scholar.claim_email is None or claim.claimed_scholar.claim_email == "":
            claim.claimed_scholar.claim_email = claim.claim_email
        else:
            claim.claimed_scholar.claim_email += "," + claim.claim_email
        claim.claimed_scholar.save()
        user.claimed_scholar = claim.claimed_scholar
        user.save()
        scholar_id = claim.claimed_scholar.es_id
        claim.delete()
        claim_email = claim.claim_email
        domain_evolve(claim_email, claim_email_special, scholar_id)
    return JsonResponse({'errno': 0, 'errmsg': '处理成功'})


def handle_appeal(request):
    if request.method != "POST":
        return JsonResponse({'errno': 1001, 'errmsg': '请求方法错误'})
    body = json.loads(request.body)
    user = auth_token(body.get("token"), True)
    if user is None or user is False:
        return JsonResponse({'errno': 1002, 'errmsg': '登录错误'})
    affair_id = body.get("affair_id")
    if affair_id is None or not Affair.objects.filter(id=affair_id).exists():
        return JsonResponse({'errno': 1003, 'errmsg': '事务不存在'})
    affair = Affair.objects.get(id=affair_id)
    if affair.type != 2:
        return JsonResponse({'errno': 1007, 'errmsg': '事务类型错误'})
    user = affair.user
    handle_reason = body.get("handle_reason")
    if handle_reason is None:
        return JsonResponse({'errno': 1004, 'errmsg': '缺少处理理由'})
    decision = body.get("decision")
    # 0 申诉无效 1 撤销对方身份 2 撤销对方身份并获得学者身份
    if decision is None:
        return JsonResponse({'errno': 1005, 'errmsg': '缺少处理决定'})
    if decision == 0:
        noticeClass.SendEmail(data=noticeClass.data,
                              receiver=user.email,
                              time=affair.submit_time.strftime("%Y-%m-%d %H:%M:%S"),
                              affair_name="申诉",
                              username=user.username,
                              decision="申诉无效",
                              reason=handle_reason).send_email(1)
        affair.appeal.delete()
    elif decision == 1:
        temp_id = affair.appeal.appealed_scholar.claimed_user_id
        if not User.objects.filter(id=temp_id).exists():
            return JsonResponse({'errno': 1006, 'errmsg': '用户不存在'})
        user2 = User.objects.get(id=temp_id)
        noticeClass.SendEmail(data=noticeClass.data,
                              receiver=user.email,
                              time=affair.submit_time.strftime("%Y-%m-%d %H:%M:%S"),
                              affair_name="申诉",
                              username=user.username,
                              decision="撤销对方身份",
                              reason=handle_reason).send_email(1)
        noticeClass.SendEmail(data=noticeClass.data,
                              receiver=user2.email,
                              time=affair.submit_time.strftime("%Y-%m-%d %H:%M:%S"),
                              affair_name="申诉",
                              username=user.username,
                              decision="被撤销身份",
                              reason=handle_reason).send_email(2)
        user2.claimed_scholar = None
        appeal = affair.appeal
        appeal.appealed_scholar.claimed_user_id = None
        appeal.appealed_scholar.save()
        appeal.delete()
    elif decision == 2:
        if user.claimed_scholar is not None:
            return JsonResponse({'errno': 1008, 'errmsg': '已经认领了学者身份'})
        temp_id = affair.appeal.appealed_scholar.claimed_user_id
        if not User.objects.filter(id=temp_id).exists():
            return JsonResponse({'errno': 1006, 'errmsg': '用户不存在'})
        user2 = User.objects.get(id=temp_id)
        appeal_email = affair.appeal.appeal_email
        appeal_email_special = body.get("appeal_email_special")
        if appeal_email_special is None:
            appeal_email_special = 0
        noticeClass.SendEmail(data=noticeClass.data,
                              receiver=user.email,
                              time=affair.submit_time.strftime("%Y-%m-%d %H:%M:%S"),
                              affair_name="申诉",
                              username=user.username,
                              decision="撤销对方身份并获得学者身份",
                              reason=handle_reason).send_email(1)
        noticeClass.SendEmail(data=noticeClass.data,
                              receiver=user2.email,
                              time=affair.submit_time.strftime("%Y-%m-%d %H:%M:%S"),
                              affair_name="申诉",
                              username=user.username,
                              decision="撤销对方身份并获得学者身份",
                              reason=handle_reason).send_email(2)
        appeal = affair.appeal
        scholar = appeal.appealed_scholar
        scholar.claimed_user_id = user.id
        if scholar.claim_email is None or scholar.claim_email == "":
            scholar.claim_email = appeal_email
        else:
            scholar.claim_email += "," + appeal_email
        scholar.save()
        user.claimed_scholar = scholar
        user.save()
        user2.claimed_scholar = None
        user2.save()
        appeal.delete()
        domain_evolve(appeal_email, appeal_email_special, scholar.es_id)
    return JsonResponse({'errno': 0, 'errmsg': '处理成功'})


def domain_evolve(claim_email, claim_email_special, scholar_id):
    if claim_email_special != 0:
        temp_email_domain = claim_email.split("@")[1].split(".")
        temp = "./Author/domains/evolving/"
        temp1 = "./Author/domains/"
        temp2 = "./Author/domains/common/"
        j = len(temp_email_domain)
        while j > 1:
            temp += temp_email_domain[j - 1] + "/"
            temp1 += temp_email_domain[j - 1] + "/"
            j -= 1
        temp1 += temp_email_domain[0] + '.txt'
        temp2 += temp_email_domain[0] + '.txt'
        if os.path.exists(temp1) or os.path.exists(temp2):
            return
        if not os.path.exists(temp):
            os.makedirs(temp)
        temp += temp_email_domain[0] + '.json'
        search_body = {
            "query": {
                "match": {
                    "id": scholar_id
                }
            }
        }
        result = es_search.body_search("authors", search_body)
        institution = es_handle.institution_field_handle(result['hits']['hits'][0]['_source'].get('institution', ""))
        if len(institution) == 0:
            return
        institution = institution[0]
        if not os.path.exists(temp):
            data = {
                "total": 0,
                "normal": 0,
                "most": institution["id"],
                "institutions": {
                    institution["id"]: {
                        "name": institution["name"],
                        "total": 0,
                    }
                }
            }
        else:
            with open(temp, "r", encoding="utf-8") as f:
                data = json.load(f)
        data["total"] += 1
        if claim_email_special == -1:
            data["normal"] += 1
        else:
            data["institutions"][institution["id"]]["total"] += 1
            if data["institutions"][institution["id"]]["total"] > data["institutions"][data["most"]]["total"]:
                data["most"] = institution["id"]
        exp = (data["institutions"][data["most"]]["total"] - 2 * data["normal"]) / data["total"]
        if exp > 0.7 and data["total"] >= 5:
            temp0 = temp1.split('/')[:-1]
            temp0 = '/'.join(temp0)
            if not os.path.exists(temp0):
                os.makedirs(temp0)
            name = data["institutions"][data["most"]]["name"]
            with open(temp1, "w", encoding="utf-8") as f:
                f.write(name)
            os.remove(temp)
        elif exp < - 0.8 and data["total"] >= 5:
            temp0 = temp2.split('/')[:-1]
            temp0 = '/'.join(temp0)
            if not os.path.exists(temp0):
                os.makedirs(temp0)
            with open(temp2, "w", encoding="utf-8") as f:
                f.write("common")
            os.remove(temp)
        else:
            with open(temp, "w", encoding="utf-8") as f:
                json.dump(data, f)

def add_admin(request):
    if request.method != "POST":
        return JsonResponse({'errno': 1001, 'errmsg': '请求方法错误'})
    body = json.loads(request.body)
    user = auth_token(body.get("token"), True)
    if user is None or user is False:
        return JsonResponse({'errno': 1002, 'errmsg': '登录错误'})
    username = body.get("username")
    password = body.get("password")
    if username is None:
        return JsonResponse({'errno': 1003, 'errmsg': '缺少用户名'})
    if password is None:
        return JsonResponse({'errno': 1004, 'errmsg': '缺少密码'})
    if Admin.objects.filter(username=username).exists():
        return JsonResponse({'errno': 1005, 'errmsg': '用户名已存在'})
    admin = Admin(username=username, password=md5_encrypt(password))
    admin.save()
    return JsonResponse({'errno': 0, 'errmsg': '添加成功'})