from django.urls import re_path
from django.contrib.auth.views import login, logout

from . import views

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^signup/$', views.signup, name='signup'),
    re_path(r'^login/$', login, name='login'),
    re_path(r'^logout/$', logout, {'next_page': 'login'}, name='logout'),
]