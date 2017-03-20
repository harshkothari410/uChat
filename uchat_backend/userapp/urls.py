"""
	smartsplit userapp URL Configuration
"""

from django.conf.urls import url
from django.contrib import admin

from . import views

app_name = 'userapp'


urlpatterns = [
	url(r'^friend/$', views.show_friend, name='show_friend'),
	url(r'^friend/add/$', views.add_friend, name='add_friend'),
	url(r'^friend/add/(?P<add_friend_detail>[-\w.]+)/$', views.add_friend_to_db, name='add_friend_to_db'),

]
