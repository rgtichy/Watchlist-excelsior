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


app_name="watchlists"

urlpatterns = [
    re_path(r'^$',                            views.index,         name = 'index'),
    re_path(r'^head/add/$',                   views.add,           name = 'add'),
    re_path(r'^head/create/$',                views.create,        name = 'create'),
    re_path(r'^head/(?P<id>\d+)/edit$',       views.edit,          name = 'edit'),
    re_path(r'^head/(?P<id>\d+)/upd$',        views.update,        name = 'update'),
    re_path(r'^head/(?P<id>\d+)/destroy$',    views.destroy,       name = 'delete'),
    re_path(r'^head/(?P<h_id>\d+)/add$',      views.add_col,       name = 'add_column'),
    re_path(r'^head/(?P<h_id>\d+)/addticker$',views.add_ticker,    name = 'add_ticker'),
    re_path(r'^view/(?P<id>\d+)'             ,views.view,          name = 'view'),
    re_path(r'^play$',                         views.playground,    name = 'playground'),               
]
