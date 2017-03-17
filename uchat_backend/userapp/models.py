from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.apps import apps
from django.contrib import admin


# Create your models here.

class UserProfile(models.Model):
	"""
	Model for uChat User
	"""
	user = models.OneToOneField(User)
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

	



class Friend(models.Model):
	"""
	Model for friend relationship
	"""
	user1 = models.ForeignKey(UserProfile, related_name="user1")
	user2 = models.ForeignKey(UserProfile, related_name="user2")
	room = models.ForeignKey('groupapp.Group', related_name="friend_group", null = True)
	created_at = models.DateTimeField(auto_now_add=True)
	modified_at = models.DateTimeField(auto_now=True)

	def rel_name(self):
		return str(self.user1) + ' Friends with ' + str(self.user2)

	def __str__(self):
		return str(self.user1) + ' Friends with ' + str(self.user2)