from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from datetime import timedelta


# Create your models here.
class ChatRoom(models.Model):
	"""
	Model for Chat Room
	"""
	name = models.TextField()
	label = models.SlugField(unique=True)

	def __unicode__(self):
		return self.label


class Message(object):
	"""
	Model for Messages
	"""
	room = models.ForeignKey(ChatRoom, related_name='messages')
	handle = models.TextField()
	message = models.TextField()
	timestamp = models.DateTimeField(default=timezone.now, db_index=True)


	def __unicode__(self):
		return '[{timestamp}] {handle}: {message}'.format(**self.as_dict())

	@property
	def formatted_timestamp(self):
		return self.timestamp.strftime('%b %-d %-I:%M %p')

	def as_dict(self):
		return {'handle': self.handle, 'message': self.message, 'timestamp': self.formatted_timestamp}

	def get_time_diff(self):
		"""
		Utilize only for seconds not minutes or seconds
		"""
		now = timezone.now()
		timediff = now - self.timestamp
		whole_diff = str(timediff)
		in_seconds = timediff.seconds
		final_date = ''

		# if difference is in days start with days
		if 'days' in whole_diff:
			final_date = whole_diff.split(',')[0] + ' ago'
		elif in_seconds < 60:
			final_date = str(in_seconds) + ' seconds ago'
		elif in_seconds < 3600:
			final_date = str(in_seconds/60) + ' minutes ago'
		else:
			final_date = str(in_seconds/3600) + ' hours ago'

		return final_date