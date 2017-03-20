from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import *
from django.urls import reverse
from django.db.models import Q

from chatapp.models import ChatRoom, Message
from userapp.models import UserProfile, Friend
# Create your views here.

def add_friend(request, user_name):
	if request.user.is_authenticated():
		loggeduser = UserProfile.objects.get(username=user_name)
		if request.method == 'POST':
			add_user = request.POST['add_user']

			# check if it is present in database or not

			try:
				if '@' in add_user:
					add_friend = UserProfile.objects.get(email=add_user)
				else:
					add_friend = UserProfile.objects.get(username=add_user)

				if add_friend == loggeduser:
					error = 'You cannot be friend with yourself'
					add_friend = None
					return render(request, 'user/add_friend.html', locals())
				return render(request, 'user/add_friend.html', locals())

			except:
				error = 'no user found with this credential please type valid one'

				return render(request, 'user/add_friend.html', locals())
			
		# return render(request, 'user/add_friend.html', locals())
	return render(request, 'user/add_friend.html', locals())

def add_friend_to_db(request, user_name, add_friend_detail):
	if request.user.is_authenticated():
		loggeduser = UserProfile.objects.get(username=user_name)

		if '@' in add_friend_detail:
			add_member = UserProfile.objects.get(email=add_friend_detail)
		else:
			add_member = UserProfile.objects.get(username=add_friend_detail)

		name = loggeduser.username + '-' + add_member.username
		description = "This is friend group for " + name
		
		label = loggeduser.username + '_' + add_member.username
		room = ChatRoom.objects.create(name=name, label=label)
		Friend.objects.create(user1=loggeduser, user2=add_member, room=room)
		Friend.objects.create(user2=loggeduser, user1=add_member, room=room)

		
		return HttpResponseRedirect(reverse('userapp:show_friend', kwargs={'user_name': loggeduser.username} ))
	return render(request, 'user/add_friend.html', locals())


def show_friend(request, user_name):
	if request.user.is_authenticated():
		live_header = 'friend'
		loggeduser = UserProfile.objects.get(username=user_name)
		return render(request, 'user/show_friend.html', locals())
	return render(request, 'user/show_friend.html', locals())