from django.contrib.auth.models import User
from models import UserProfile, Friend
from rest_framework import serializers
from chatapp.models import ChatRoom, Message, ChatRoomMember
# from views import UserProfileDetail

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('pk', 'username', 'password', 'email')

class UserProfileSerializer(serializers.ModelSerializer):
	# url = serializers.HyperlinkedIdentityField(
	# 	view_name='views.UserProfileDetail',
	# 	lookup_field='username'
	# )

	# print serializers.HyperlinkedModelSerializer.__dict__

	class Meta:
		model = UserProfile
		fields = ('first_name', 'last_name', 'user', 'username', 'email', 'created_at', 'url',)
		extra_kwargs = {
			'url': {'view_name': 'user-detail', 'lookup_field': 'username'},
			# 'users': {'lookup_field': 'username'}
		}

class UserFriendSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = Friend
		fields = ('friend', 'room', 'created_at', 'modified_at')
		depth = 1

	# def create(self, validated_data):
	# 	print validated_data
		# data = request.data
		# s = Friend.objects.create()

	# 	return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class ChatRoomSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = ChatRoom
		fields = ('name', 'label', 'created_at', 'modified_at')
		depth = 1

class MessageSerializer(serializers.ModelSerializer):
	class Meta:
		model = Message
		fields = ('room', 'handle', 'message', 'timestamp')

class GroupMemberSerializer(serializers.ModelSerializer):
	class Meta:
		model = ChatRoomMember
		fields = ('user',)
		depth = 1