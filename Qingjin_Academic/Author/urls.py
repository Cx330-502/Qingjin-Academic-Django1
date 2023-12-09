from django.urls import path
from .views import *

urlpatterns = [
    # path('url_name', api_name)
    # 这是一个样例，指定路由名为url_name，对应处理函数为当前app内views.py中的api_name
    path('email_claim', email_claim),
    path('other_claim', other_claim),
    path('appeal_author', appeal_author),
]
