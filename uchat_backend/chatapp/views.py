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

def test(request):
	if request.user.is_authenticated():
		room, created = ChatRoom.objects.get_or_create(label='47716bb0-5f9b-4676-9474-706cc95dc801')
		loggeduser = UserProfile.objects.get(username=request.user)
		messages = reversed(room.messages.order_by('-timestamp')[:50])
		return render(request, 'chat/index.html', locals())
	return render(request, 'chat/index.html', locals())

def index(request):
	if request.user.is_authenticated():
		loggeduser = UserProfile.objects.get(username=request.user)
		return redirect( '/chat', loggeduser = loggeduser )
	return render(request, 'login_signup.html', locals())

def chat_dashboard(request):
	return render(request, 'chat_index.html', locals())

def user_login(request):
	if request.user.is_authenticated():
		loggeduser = UserProfile.objects.get(username=request.user)
		return redirect( '/chat', loggeduser = loggeduser )

	print "Hello"
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']

		username = username.lower()
		# print User.objects.get(username=username, password=password)
		user = authenticate(username=username, password=password)

		print username, password, user
		if user:
			login(request, user)
			loggeduser = UserProfile.objects.get(username = username)
			return redirect( '/chat', loggeduser = loggeduser )

	return render(request, 'login_signup.html', locals())

def signup(request):
	if request.user.is_authenticated():
		loggeduser = UserProfile.objects.get(username=request.user)
		return redirect( '/chat', loggeduser = loggeduser )

	if request.method == 'POST':
		first_name = request.POST['first_name']
		last_name = request.POST['last_name']

		username = request.POST['username']
		password = request.POST['password']

		email = request.POST['email']
		username = username.lower()

		print first_name, last_name, email, username, password
		try:
			otheruser = UserProfile.objects.get(username = username)
			error = 'This Username already exists...'

			return render(request, 'login_signup.html', locals())

		except:
			pass

		try:
			otheruser = UserProfile.objects.get(email = email)
			error = 'This Email already exists...'
			return render(request, 'login_signup.html', locals())

		except:
			pass

		try:
			user = User.objects.create_user(username=username, password=password, email=email)
			user = authenticate(username=username, password=password)

			login(request, user)

			loggeduser = UserProfile.objects.get_or_create(username=username, user = user, first_name=first_name, last_name=last_name, email=email)

		except Exception as e:
			print e, e.__dict__
			error = 'Validation Error...'
			return render(request, 'login_signup.html', locals())

		return redirect( '/chat', loggeduser = loggeduser )

def user_logout(request):
	logout(request)
	return redirect('/')

def chatroom(request, label):
	"""
	Function : chatroom

	@input
		label

	@output
		HTTPResponse
	"""

	# If the room with the given label doesn't exist, automatically create it

	if request.user.is_authenticated():
		room, created = ChatRoom.objects.get_or_create(label='47716bb0-5f9b-4676-9474-706cc95dc801')
		loggeduser = UserProfile.objects.get(username=request.user)
		# try:
		# 	users = Friend.objects.filter(room=room)
		# 	print users
		# 	u_list = []
		# 	for u in users:
		# 		u_list.append(u.creator.username)
			
		# 	print u_list, request.user.username
		# 	print request.user.username in u_list
		# 	if request.user.username not in u_list:
		# 		error = 'You are not authenticate for this'
		# 		print "I am here"
		# 		return redirect('/')
		# except:
		# 	error = 'You are not authenticate for this'
		# 	return redirect('/')

		# messages = reversed(room.messages.order_by('-timestamp')[:50])
		friends = loggeduser.get_friends()
		groups = loggeduser.get_group()
		return render(request, 'chat/index.html', locals())

	return redirect('/')


	




