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
from django.conf.urls import url, include
from django.contrib import admin
import userapp
from chatapp import views
from userapp import views as views1


from rest_framework.urlpatterns import format_suffix_patterns

from rest_framework import routers
router = routers.DefaultRouter()

# router.register(r'users', views1.UserProfileViewSet)

urlpatterns = [
    # url(r'^', include(router.urls)),
    url(r'^api/v1/users/$', views1.UserProfileList.as_view(), name='user-list'),
    url(r'^api/v1/users/(?P<username>[-\w.]+)/$', views1.UserProfileDetail.as_view(), name='user-detail'),
    url(r'^api/v1/users/(?P<username>[-\w.]+)/friends/$', views1.UserFriendList.as_view(), name='user-friend-list'),
    url(r'^api/v1/users/(?P<username>[-\w.]+)/friends/(?P<friend>[-\w.]+)/$', views1.UserFriendDetail.as_view(), name='user-friend-detail'),
    url(r'^api/v1/users/(?P<username>[-\w.]+)/friends/(?P<friend>[-\w.]+)/chats/$', views1.UserFriendChat.as_view(), name='user-friend-chat-list'),
    # url(r'^api/v1/groups/(?P<group>[-\w.]+)/friends/(?P<friend>[-\w.]+)/chats/$', views1.UserFriendChat.as_view(), name='user-friend-chat-list'),
    

    # Group related URL
    url(r'^api/v1/groups/$', views1.GroupList.as_view(), name='group-list'),
    url(r'^api/v1/groups/(?P<group>[-\w.]+)/$', views1.GroupDetail.as_view(), name='group-detail'),
    url(r'^api/v1/groups/(?P<group>[-\w.]+)/members/$', views1.GroupMemberList.as_view(), name='group-member-list'),
    url(r'^api/v1/groups/(?P<group>[-\w.]+)/members/(?P<username>[-\w.]+)/$', views1.GroupMemberDetail.as_view(), name='group-member-detail'),

    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name="index" ),
    url(r'^login/$', views.user_login, name="user_login"),
    url(r'^signup/$', views.signup, name="signup"),
    url(r'^logout/$', views.user_logout, name="logout"),

    url(r'^test/test/$', views.test, name="test"),    
    # url(r'^chat/$', views.chatroom, name='chat_room'),

    url(r'^(?P<label>[\w-]{,50})/$', views.chatroom, name='chat_room_1'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
    # url(r'^api/v1/user/(?P<user_name>[-\w.]+)/$', views1.get_user, name='userapp-api-url'),
    # Userapp URLs
    # url(r'^(?P<user_name>[-\w.]+)/', include('userapp.urls', namespace='userapp-url')),

    
]

urlpatterns = format_suffix_patterns(urlpatterns)