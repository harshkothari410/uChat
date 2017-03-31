from django.contrib.auth.models import User
from models import UserProfile
from rest_framework import serializers
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
		fields = ('first_name', 'last_name', 'user', 'username', 'email', 'created_at', 'url')
		extra_kwargs = {
			'url': {'view_name': 'user-detail', 'lookup_field': 'username'},
			# 'users': {'lookup_field': 'username'}
		}
		

		# users = serializers.HyperlinkedRelatedField(
		# 	view_name='UserProfileDetail',
		# 	lookup_field='username',
		# 	many=True,
		# 	read_only=True
		# )