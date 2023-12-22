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


def comment(request):
    if request.method != "POST":
        return JsonResponse({'errno': 1001, 'errmsg': '请求方法错误'})
    body = json.loads(request.body)
    user = auth_token(body.get("token"), False)
    if user is None or user is False:
        return JsonResponse({'errno': 1002, 'errmsg': '登录错误'})
    paper_id = body.get("paper_id")
    content = body.get("content")
    if content is None or content == "":
        return JsonResponse({'errno': 1002, 'errmsg': '请传入合法的评论'})
    reply_to = body.get("reply_to")
    if reply_to is not None and not Comment.objects.filter(id=reply_to).exists():
        return JsonResponse({'errno': 1003, 'errmsg': '回复的评论不存在'})
    if reply_to is not None:
        reply_to = Comment.objects.get(id=reply_to)
        if reply_to.reply_to is not None:
            comment0 = Comment(user=user, paper_id=paper_id, content=content, reply_to=reply_to)
    else:
        comment0 = Comment(user=user, paper_id=paper_id, content=content)
    comment0.save()
    return JsonResponse({'errno': 0,
                         'errmsg': '评论成功',
                         'data': {
                             'comment_id': comment0.id,
                             'comment_time': comment0.comment_time.strftime("%Y-%m-%d %H:%M:%S"),
                         }})


def get_comment(request):
    if request.method != "POST":
        return JsonResponse({'errno': 1001, 'errmsg': '请求方法错误'})
    body = json.loads(request.body)
    paper_id = body.get("paper_id")
    comments = Comment.objects.filter(paper_id=paper_id).order_by('id')
    return_table = {}
    for comment0 in comments:
        is_scholar = False
        author_id = ""
        if comment0.user.claimed_scholar is not None:
            is_scholar = True
            author_id = comment0.user.claimed_scholar.es_id
        if comment0.reply_to is not None:
            if comment0.reply_to.reply_to is not None:
                return_user_name = comment0.reply_to.user.username
            else:
                return_user_name = ""
            temp = comment0.reply_to
            while temp.reply_to is not None:
                temp = temp.reply_to
            if temp.id in return_table:
                data = {
                    "id": comment0.id,
                    "user": comment0.user.username,
                    "user_id": comment0.user.id,
                    "comment_time": comment0.comment_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "content": comment0.content,
                    "is_scholar": is_scholar,
                    "author_id": author_id,
                    "reply_to": return_user_name
                }
                return_table[temp.id]['reply_list'].append(data)
                continue
        data = {
            "id": comment0.id,
            "user": comment0.user.username,
            "user_id": comment0.user.id,
            "comment_time": comment0.comment_time.strftime("%Y-%m-%d %H:%M:%S"),
            "content": comment0.content,
            "is_scholar": is_scholar,
            "author_id": author_id,
            "reply_list": []
        }
        return_table[comment0.id] = data
    return_list = []
    for key in return_table:
        return_list.append(return_table[key])
    return JsonResponse({'errno': 0,
                         'errmsg': '获取评论成功',
                         'data': return_list})


def delete_comment(request):
    if request.method != "POST":
        return JsonResponse({'errno': 1001, 'errmsg': '请求方法错误'})
    body = json.loads(request.body)
    user = auth_token(body.get("token"), False)
    if user is None or user is False:
        return JsonResponse({'errno': 1002, 'errmsg': '登录错误'})
    comment_id = body.get("comment_id")
    if comment_id is None or comment_id == "":
        return JsonResponse({'errno': 1003, 'errmsg': '缺少评论id'})
    if not Comment.objects.filter(id=comment_id).exists():
        return JsonResponse({'errno': 1004, 'errmsg': '评论不存在'})
    comment0 = Comment.objects.get(id=comment_id)
    if comment0.user != user:
        return JsonResponse({'errno': 1005, 'errmsg': '无权限删除评论'})
    comment0.delete()
    return JsonResponse({'errno': 0, 'errmsg': '删除评论成功'})


def report_comment_comment_or_paper(request):
    if request.method != "POST":
        return JsonResponse({'errno': 1001, 'errmsg': '请求方法错误'})
    body = request.POST.copy()
    user = auth_token(body.get("token"), False)
    if user is None or user is False:
        return JsonResponse({'errno': 1002, 'errmsg': '登录错误'})
    paper_id = body.get("paper_id")
    comment_id = body.get("comment_id")
    report_text = body.get("report_text")
    report_file = request.FILES.get("report_file")
    if paper_id is None or paper_id == "":
        return JsonResponse({'errno': 1003, 'errmsg': '缺少举报对象'})
    if report_text is None and report_file is None:
        return JsonResponse({'errno': 1004, 'errmsg': '缺少举报内容'})
    if comment_id is not None and comment_id != -1:
        if not Comment.objects.filter(id=comment_id).exists():
            return JsonResponse({'errno': 1005, 'errmsg': '评论不存在'})
        comment0 = Comment.objects.get(id=comment_id)
        if comment0.user == user:
            return JsonResponse({'errno': 1006, 'errmsg': '不能举报自己的评论'})
        if report_text is None:
            report = Report(paper_id=paper_id, comment=comment0)
            report.save()
            report.report_file = report_file
        elif report_file is None:
            report = Report(paper_id=paper_id, comment=comment0, report_text=report_text)
        else:
            report = Report(paper_id=paper_id, comment=comment0, report_text=report_text)
            report.save()
            report.report_file = report_file
    else:
        if report_text is None:
            report = Report(paper_id=paper_id)
            report.save()
            report.report_file = report_file
        elif report_file is None:
            report = Report(paper_id=paper_id, report_text=report_text)
        else:
            report = Report(paper_id=paper_id, report_text=report_text)
            report.save()
            report.report_file = report_file
    report.save()
    affair = Affair(report=report, user=user, type=1, submit_time=datetime.datetime.now(), status=0)
    affair.save()
    return JsonResponse({'errno': 0, 'errmsg': '举报成功'})


def get_paper_information(request):
    if request.method != "POST":
        return JsonResponse({'errno': 1001, 'errmsg': '请求方法错误'})
    body = json.loads(request.body)
    user = auth_token(body.get('token'), False)
    paper_id = body.get("paper_id")
    if paper_id is None:
        return JsonResponse({'errno': 1002, 'errmsg': '缺少论文id'})
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
    result = es_handle.handle_detailed_work(result["hits"]["hits"][0])
    result = es_handle.star_handle([result], user, 0)[0]
    return JsonResponse({'errno': 0, 'errmsg': 'success', 'data': result})
