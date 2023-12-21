from django.urls import path
from .views import *

urlpatterns = [
    # path('url_name', api_name)
    # 这是一个样例，指定路由名为url_name，对应处理函数为当前app内views.py中的api_name
    path('user/captcha', captcha, name='captcha'),
    path('user/register', user_register),
    path('user/login', user_login),
    path('user/change_password', change_password),
    path('hot_paper', hot_paper),
    path('hot_institution', hot_institution),
    path('delete_history', delete_history),
    path('clear_history', clear_history),
    path('get_history', get_history),
    path('get_stars', get_stars),
    path('get_folders', get_folders),
    path('unstar', unstar),
    path('create_folder', create_folder),
    path('move_star', move_star),
    path('delete_folder', delete_folder),

    path('add_history', add_history),
    path('star', star),

    path('get_chat_history', get_chat_history),
    path('ai_chat', ai_chat),
    path('clear_ai_history', clear_ai_history)
]
