from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.apps import apps
from django.contrib import admin
import operator

import chatapp
# from chatapp import ChatRoomMember
# Create your models here.

class UserProfile(models.Model):
	"""
	Model for uChat User
	"""
	user = models.OneToOneField(User, null=True)
	first_name = models.CharField(max_length=255, blank = True, null = True)
	last_name = models.CharField(max_length=255, blank = True, null = True)
	username = models.CharField(max_length=255, blank = True, null = True)
	email = models.EmailField(max_length=254, blank=True, null=True)
	groups = models.CharField(max_length=500, blank = True, null = True)
	created_at = models.DateTimeField(auto_now_add=True)
	modified_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.first_name + ' - ' + self.username

	def name(self):
		return self.first_name + ' ' + self.last_name

	
	def get_friends(self):
		bot = UserProfile.objects.get(username='uChat-bot')
		return sorted(Friend.objects.filter(creator=self).exclude(friend=bot), key=operator.attrgetter('room.modified_at'), reverse=True)

	def get_group(self):
		return chatapp.models.ChatRoomMember.objects.filter(user=self)

	def get_bot(self, bot):
		# uchatbot = models.objects.get(username='uChat-bot')
		return Friend.objects.get(creator=self, friend=bot)


class Friend(models.Model):
	"""
	Model for friend relationship
	"""
	creator = models.ForeignKey(UserProfile, related_name="user1", null=True)
	friend = models.ForeignKey(UserProfile, related_name="friend", null=True)
	room = models.ForeignKey('chatapp.ChatRoom', related_name="chat_room", null = True, default=None)
	created_at = models.DateTimeField(auto_now_add=True)
	modified_at = models.DateTimeField(auto_now=True)

	def rel_name(self):
		return str(self.user1) + ' Friends with ' + str(self.user2)

	def __str__(self):
		return str(self.creator) + ' Friends with ' + str(self.friend)

