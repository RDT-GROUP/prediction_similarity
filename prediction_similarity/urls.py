"""prediction_similarity URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path,re_path
from web import views
from django.conf.urls import url
from django.views.static import serve
from prediction_similarity import settings
urlpatterns = [    
    #detail?id=123123
    url(r'detail/$', views.detail),

    #detail?type=1&query="123123"
    url(r'result/$', views.result),

    url(r'test/$',views.test),

    url(r'^$', views.index),
    url(r'media/(?P<path>.*)$',serve,{'document_root':settings.MEDIA_ROOT}),
]
