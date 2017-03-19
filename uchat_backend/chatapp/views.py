from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import *
from django.urls import reverse
from django.db.models import Q

from chatapp.models import ChatRoom, Message
from userapp.models import UserProfile

# Create your views here.

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

	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']

		username = username.lower()
		user = authenticate(username=username, password=password)

		print username, password
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
	room, created = ChatRoom.objects.get_or_create(label=label)

	messages = reversed(room.messages.order_by('-timestamp')[:50])

	return render(request, 'chat.html', locals())