from django.contrib.auth.models import User
from django.db import models
from www.models import *


class StaffDictionary(models.Model):
	"""
	StaffDictionary is a dictionary for different values needed
	within the Staff App Context
	"""
	key = models.CharField(max_length=255)
	value = models.TextField(blank=True, null=True)

	def __unicode__(self):
		return "<key=%s>" % (self.key)
		

class Attendance(models.Model):
	"""
	Attendance of users in events
	"""
	user = models.ForeignKey(User, related_name='attended')
	event = models.ForeignKey(Event)
	timestamp = models.DateTimeField(auto_now_add=True)
	scored_by = models.ForeignKey(User, related_name='scores')

	def was_enrolled(self):
		return self.user in self.event.users_enrolled.all()
	def __unicode__(self):
		return "<%s attended to %s on %s>" % (self.user, self.event.name, self.timestamp)

