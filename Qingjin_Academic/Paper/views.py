import datetime

from django.http import JsonResponse
from django.shortcuts import render
import json
# Create your views here.
from Academic_models.models import *


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
    comments = Comment.objects.filter(paper_id=paper_id).order_by('-top')
    return_list = []
    for comment0 in comments:
        data = {
            "id": comment0.id,
            "user": comment0.user.username,
            "comment_time": comment0.comment_time.strftime("%Y-%m-%d %H:%M:%S"),
            "content": comment0.content,
            "top": comment0.top
        }
        return_list.append(data)
    return JsonResponse({'errno': 0,
                         'errmsg': '获取评论成功',
                         'data': return_list})


def report_comment_comment_or_paper(request):
    if request.method != "POST":
        return JsonResponse({'errno': 1001, 'errmsg': '请求方法错误'})
    body = json.loads(request.body)
    user = auth_token(body.get("token"), False)
    if user is None or user is False:
        return JsonResponse({'errno': 1002, 'errmsg': '登录错误'})
    paper_id = body.get("paper_id")
    comment_id = body.get("comment_id")
    report_text = body.get("report_text")
    report_file = body.get("report_file")
    if paper_id is None:
        return JsonResponse({'errno': 1003, 'errmsg': '缺少举报对象'})
    if report_text is None and report_file is None:
        return JsonResponse({'errno': 1004, 'errmsg': '缺少举报内容'})
    if comment_id is not None:
        if not Comment.objects.filter(id=comment_id).exists():
            return JsonResponse({'errno': 1005, 'errmsg': '评论不存在'})
        comment0 = Comment.objects.get(id=comment_id)
        if comment0.user == user:
            return JsonResponse({'errno': 1006, 'errmsg': '不能举报自己的评论'})
        if report_text == None:
            report = Report(paper_id=paper_id, comment=comment0, report_file=report_file)
        elif report_file == None:
            report = Report(paper_id=paper_id, comment=comment0, report_text=report_text)
        else:
            report = Report(paper_id=paper_id, comment=comment0, report_text=report_text, report_file=report_file)
    else:
        if report_text == None:
            report = Report(paper_id=paper_id, report_file=report_file)
        elif report_file == None:
            report = Report(paper_id=paper_id, report_text=report_text)
        else:
            report = Report(paper_id=paper_id, report_text=report_text, report_file=report_file)
    report.save()
    affair = Affair(report=report, user=user, type=1, submit_time=datetime.datetime.now(), status=0)
    return JsonResponse({'errno': 0, 'errmsg': '举报成功'})
