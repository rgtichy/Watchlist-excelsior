from django.conf.urls import url, include
from . import views

app_name='userprofiles'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'register$',views.register, name='create'),
    url(r'login$',views.login, name='login'),
    url(r'landingpage/$', views.landingpage, name='success'),
    url(r'logout$',views.logout, name='logout')
]
