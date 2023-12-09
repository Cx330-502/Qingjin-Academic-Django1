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
    paper_id = body.get("paper_id");
    content = body.get("content");
    if content is None or content == "":
        return JsonResponse({'errno': 1002, 'errmsg': '请传入合法的评论'})
    comment = Comment(paper_id, content)
    comment.save()
    return JsonResponse({'errno': 0,
                         'errmsg': '评论成功',
                         'data':{
                             'comment_id': comment.id
                         }})


def get_comment(request):
    if request.method != "POST":
        return JsonResponse({'errno': 1001, 'errmsg': '请求方法错误'})
    body = json.loads(request.body)
    paper_id = body.get("paper_id")
    comments = Comment.objects.filter(paper_id=paper_id).order_by('-top')
    return_list = []
    for comment in comments:
        data = {
            "id": comment.id,
            "content": comment.content,
            "star_num": comment.star_num,
            "top": comment.top
        }
        return_list.append(data)
    return JsonResponse({'errno': 0,
                         'errmsg': '获取评论成功',
                         'data': return_list})


