from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import *
from django.urls import reverse

from chatapp.models import ChatRoom, Message

# Create your views here.

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