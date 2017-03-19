"""uchat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from chatapp import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name="index" ),
    url(r'^login/$', views.user_login, name="user_login"),
    url(r'^signup/$', views.signup, name="signup"),
    url(r'^logout/$', views.user_logout, name="logout"),

    url(r'^chat/$', views.chat_dashboard, name="chat_dashboard"),

    # url(r'^(?P<label>[\w-]{,50})/$', views.chatroom, name='chat_room'),
]
