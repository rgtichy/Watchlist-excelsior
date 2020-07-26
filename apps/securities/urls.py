"""
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, re_path, include
from . import views
# from scaffolding import SecurityCrudManager


app_name="securities"

urlpatterns = [
    re_path(r'^$',                           views.index,         name = 'index'),
    re_path(r'^load',                        views.load,          name = 'load'),
    re_path(r'^(?P<id>\d+)/view$',           views.security,      name = 'security'),

    re_path(r'^companies',                   views.companies,     name = 'companies'),
    re_path(r'^c_load',                      views.c_load,        name = 'c_load'),
    re_path(r'^S/(?P<id>\d+)/view$',         views.company,       name = 'company'),

    re_path(r'^datatags/add$',               views.datatag_add,   name = 'datatag_add'),
    re_path(r'^data_tag_load',               views.data_tag_load, name = 'data_tag_load'),
    re_path(r'^datatags$',                   views.datatags,      name = 'datatags'),
    re_path(r'^datatag/(?P<id>\d+)/edit$',   views.datatag,       name = 'datatag_edit'),
    re_path(r'^datatag/(?P<id>\d+)/del$',    views.data_tag_del,  name = 'datatag_delete'),

    re_path(r'^data_tag/(?P<id>\d+)/upd$',   views.data_tag_edit, name = 'data_tag_edit'),
    re_path(r'^data_tag$',                   views.data_tag,      name = 'data_tag'),
]
