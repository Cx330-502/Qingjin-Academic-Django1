from django.urls import path
from .views import *

urlpatterns = [
    # path('url_name', api_name)
    # 这是一个样例，指定路由名为url_name，对应处理函数为当前app内views.py中的api_name
    path('get_affairs', get_affairs),
    path('get_detailed_report', get_detailed_report),
    path('get_detailed_appeal', get_detailed_appeal),
    path('get_detailed_claim', get_detailed_claim),
    path('handle_report', handle_report),
    path('handle_appeal', handle_appeal),
    path('handle_claim', handle_claim),
    path('add_admin', add_admin),
]