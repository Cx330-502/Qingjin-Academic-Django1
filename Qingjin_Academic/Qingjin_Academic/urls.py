"""Qingjin_Academic URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.conf import settings
from django.urls import re_path
from django.views.static import serve

urlpatterns = [
    #    path("admin/", admin.site.urls),
    path("api/v1/admin/", include(("Admin.urls", "Admin"))),
    path("api/v1/author/", include(("Author.urls", "Author"))),
    path("api/v1/home/", include(("Home.urls", "Home"))),
    path("api/v1/institutions/", include(("Institutions.urls", "Institutions"))),
    path("api/v1/paper/", include(("Paper.urls", "Paper"))),
    path("api/v1/search_result/", include(("Search_result.urls", "Search_result"))),
    path("api/v1/academic_models/", include(("Academic_models.urls", "Academic_models"))),
    re_path('^api/v1/media/(?P<path>.*?)$', serve, kwargs={'document_root': settings.MEDIA_ROOT})

]
