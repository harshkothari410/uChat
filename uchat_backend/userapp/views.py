from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import *
from django.urls import reverse

from django.db.models import Q
from django.core import serializers
from django.forms.models import model_to_dict

from chatapp.models import ChatRoom, Message, ChatRoomMember
from userapp.models import UserProfile, Friend
import json
from django.http import JsonResponse, HttpResponseBadRequest
import uuid


# REST import
from rest_framework import viewsets
from serializers import UserProfileSerializer, UserSerializer, UserFriendSerializer, MessageSerializer, ChatRoomSerializer, GroupMemberSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
# Create your views here.

# Testing Class Based View
class UserProfileList(APIView):
	"""docstring for UserProfileList"""

	authentication_classes = (SessionAuthentication, BasicAuthentication)
	permission_classes = (IsAuthenticated,)
	def get(self, request, format=None):

		content = {
			'user': unicode(request.user),
			'auth': unicode(request.auth)
		}
		users = UserProfile.objects.all()
		serializer = UserProfileSerializer(users, many=True, context={'request': request})
		return Response(serializer.data)

	def post(self, request, format=None):
		user = UserSerializer(data=request.data)
		if user.is_valid():
			u = user.save()
		else:
			return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)
		print u
		request.data['user'] = u.pk

		serializer = UserProfileSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED, context={'request': request})
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileDetail(APIView):
	authentication_classes = (SessionAuthentication, BasicAuthentication)
	permission_classes = (IsAuthenticated,)

	def get_user(self, username):
		try:
			return UserProfile.objects.get(username=username)
		except:
			raise Http404

	def get_main_user(self, username):
		try:
			return User.objects.get(username=username)
		except:
			raise Http404

	def get(self, request, username):
		print request.user, request.auth
		content = {
			'user': unicode(request.user),
			'auth': unicode(request.auth)
		}
		user = self.get_user(username)
		serializer = UserProfileSerializer(user, context={'request': request})
		print serializer.data
		return Response(serializer.data)

	def put(self, request, username, format=None):
		user = self.get_user(username)
		main_user = self.get_main_user(username)

		# User Class update
		main_user_serializer = UserSerializer(main_user, data=request.data)
		if main_user_serializer.is_valid():
			u = main_user_serializer.save()
		else:
			return Response(main_user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

		# UserProfile Class update
		# request.data['user'] = u.pk
		user_serializer = UserProfileSerializer(user, data=request.data)
		if main_user_serializer.is_valid():
			# request.data['user'] = u.pk
			user_serializer.save()

			return Response(user_serializer.data)
		
		return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def patch(self, request, username, format=None):
		user = self.get_user(username)
		main_user = self.get_main_user(username)

		# User Class update
		main_user_serializer = UserSerializer(main_user, data=request.data, partial=True)
		if main_user_serializer.is_valid():
			u = main_user_serializer.save()
		else:
			return Response(main_user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

		# UserProfile Class update
		user_serializer = UserProfileSerializer(user, data=request.data, partial=True, context={'request': request})
		if user_serializer.is_valid():
			
			user_serializer.save()

			return Response(user_serializer.data)
		
		return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, username, format=None):
		user = self.get_user(username)
		user1 = self.get_main_user(username)
		user.delete()
		user1.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

class UserFriendList(APIView):
	authentication_classes = (SessionAuthentication, BasicAuthentication)
	permission_classes = (IsAuthenticated,)

	def get(self, request, username, format=None):
		user = UserProfile.objects.get(username=username)
		users = Friend.objects.filter(creator=user)
		serializer = UserFriendSerializer(users, many=True, context={'request': request})
		return Response(serializer.data)

	def post(self, request, username, format=None):
		creator = UserProfile.objects.get(username=username)
		friend = UserProfile.objects.get(username=request.data['username'])

		# serializer = UserProfileSerializer(friend, context={'request': request})
		# request.data['creator'] = creator
		# request.data['friend'] = friend

		# @fix me : Add Channel
		# request.data['group'] = None
		room_name = creator.username + '-' + friend.username
		room = ChatRoom.objects.create(name=room_name, label=uuid.uuid4())

		try:
			s = Friend.objects.create(creator=creator, friend=friend, room=room)
			g = Friend.objects.create(creator=friend, friend=creator, room=room)
			serializer = UserFriendSerializer(s)
			print serializer
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		except:
			pass
		
		return Response({}, status=status.HTTP_400_BAD_REQUEST)

class UserFriendDetail(APIView):
	authentication_classes = (SessionAuthentication, BasicAuthentication)
	permission_classes = (IsAuthenticated,)

	def get_friend(self, username, friend, format=None):
		try:
			creator = UserProfile.objects.get(username=username)
			friend = UserProfile.objects.get(username=friend)
			return Friend.objects.get(creator=creator, friend=friend)
		except:
			raise Http404

	def get(self, request, username, friend, format=None):
		user = self.get_friend(username, friend)
		serializer = UserFriendSerializer(user, context={'request': request})
		return Response(serializer.data)

	def delete(self, request, username, friend, format=None):
		friend = self.get_friend(username, friend)
		friend.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)


class UserFriendChat(APIView):
	authentication_classes = (SessionAuthentication, BasicAuthentication)
	permission_classes = (IsAuthenticated,)

	def get_chatroom(self, username, friend):
		print username, friend
		try:
			creator = UserProfile.objects.get(username=username)
			friend = UserProfile.objects.get(username=friend)
			return Friend.objects.get(creator=creator, friend=friend)
		except:
			raise Http404

	def get(self, request, username, friend, format=None):
		# print username, friend
		room = self.get_chatroom(username, friend).room
		# print room
		messages = reversed(room.messages.order_by('-timestamp')[:50])
		# print messages
		serializer = MessageSerializer(messages, many=True, context={'request': request})
		return Response(serializer.data)


class GroupList(APIView):
	authentication_classes = (SessionAuthentication, BasicAuthentication)
	permission_classes = (IsAuthenticated,)

	def get(self, request):
		groups = ChatRoom.objects.all()
		serializer = ChatRoomSerializer(groups, many=True, context={'request': request})
		return Response(serializer.data)

	def post(self, request):
		print request.user, request.user.username
		creator = UserProfile.objects.get(user=request.user)
		room_name = request.data['name']

		group = ChatRoom.objects.create(name=room_name, label=uuid.uuid4())

		# Add to group members

		member = ChatRoomMember.objects.create(group=group, user=creator, admin=True)

		serializer = ChatRoomSerializer(group, context={'request': request})
		return Response(serializer.data)

class GroupDetail(APIView):
	authentication_classes = (SessionAuthentication, BasicAuthentication)
	permission_classes = (IsAuthenticated,)

	def get_group(self, group):
		try:
			return ChatRoom.objects.get(label=group)
		except:
			raise Http404

	def get(self, request, group):
		group = self.get_group(group)

		serializer = ChatRoomSerializer(group, context={'request': request})
		return Response(serializer.data)

class GroupMemberList(APIView):
	authentication_classes = (SessionAuthentication, BasicAuthentication)
	permission_classes = (IsAuthenticated,)

	def get_group(self, group):
		try:
			return ChatRoom.objects.get(label=group)
		except:
			raise Http404

	def get(self, request, group):
		group = self.get_group(group)

		members = ChatRoomMember.objects.filter(group=group)
		serializer = GroupMemberSerializer(members, many=True, context={'request': request})

		return Response(serializer.data)

	def post(self, request, group):
		group = self.get_group(group)
		member = UserProfile.objects.get(username=request.data['username'])

		member = ChatRoomMember.objects.create(group=group, user=member)

		serializer = GroupMemberSerializer(member, context={'request': request})
		return Response(serializer.data)

class GroupMemberDetail(APIView):
	uthentication_classes = (SessionAuthentication, BasicAuthentication)
	permission_classes = (IsAuthenticated,)

	def get_group(self, group):
		try:
			return ChatRoom.objects.get(label=group)
		except:
			raise Http404

	def get_user(self, username):
		try:
			return UserProfile.objects.get(username=username)
		except:
			raise Http404

	def get_group_record(self, group, member):
		try:
			return ChatRoomMember.objects.get(group=group, user=member)
		except:
			raise Http404

	def get(self, request, group, username):
		print group
		group = self.get_group(group)
		member = self.get_user(username)

		group_record = self.get_group_record(group, member)

		serializer = GroupMemberSerializer(group_record, context={'request': request})
		return Response(serializer.data)


	def delete(self, requests, group, username):
		group = self.get_group(group)
		member = self.get_user(username)

		group_record = self.get_group_record(group, member)
		group_record.delete()

		return Response(status=status.HTTP_204_NO_CONTENT)



# class UserProfileViewSet(generics.ListCreateAPIView):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     queryset = UserProfile.objects.all()
#     serializer_class = UserProfileSerializer

# # Views for django rest APIs
# class UserProfileViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     queryset = UserProfile.objects.all()
#     serializer_class = UserProfileSerializer


def get_user(request, user_name):
	if request.method == 'GET':
		add_user = user_name
		# try:
		if '@' in add_user:
			add_friend = UserProfile.objects.get(email=add_user)
		else:
			print add_user
			add_friend = UserProfile.objects.get(username=add_user)
			print add_friend

		# if add_friend == loggeduser:
		# 	data = {
		# 		'error' : 'You cannot be friend with yourself',
		# 	}
		# 	error = 'You cannot be friend with yourself'
		# 	add_friend = None
		# 	return JsonResponse(data)

		print add_friend.__dict__
		data = serializers.serialize("json", [add_friend])
		# print data
		# print json.dumps(add_friend.__dict__)
		return JsonResponse(data, safe=False)

	# 	except:
	# 		data = {
	# 			'error' : 'no user found with this credential please type valid one',
	# 		}
	# 		error = 'no user found with this credential please type valid one'

	# 		return JsonResponse(data)

	# return HttpResponseBadRequest()

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

def api_add_friend(request, user_name):
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