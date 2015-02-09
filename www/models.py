# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from .choices import *

class UserProfile(models.Model):
	"""
	Extended profile of an User
	"""
	user = models.OneToOneField(User)
	dni = models.CharField(max_length=25)
	course = models.CharField(max_length=3, choices=COURSE_CHOICES, default='II')
	auto_enroll_all = models.BooleanField(default=False)

	def __unicode__(self):
		return "%s" % self.user

class Venue(models.Model):
	"""
	Model for a Venue
	"""
	name = models.CharField(max_length=255)
	latitude = models.CharField(max_length=255)
	longitude = models.CharField(max_length=255)
	
	def __unicode__(self):
		return "%s" % self.name

class TimeStripe(models.Model):
	"""
	Model for a Calendar Stripe
	"""
	day = models.IntegerField(max_length=1, choices=DAY_CHOICES, default=1)
	time_stripe = models.IntegerField(max_length=1, choices=TIME_STRIPE_CHOICES, default=1)
	duration = models.IntegerField(max_length=1, choices=DURATION_CHOICES, default=2)
	
	def __unicode__(self):
		return "(%s el %s @ %s)" % (self.get_duration_display(), self.get_day_display(), self.get_time_stripe_display())
	
	class Meta:
		ordering = ['day','time_stripe']

class Event(models.Model):
	"""
	Model for an event
	"""
	kind_of_event = models.CharField(max_length=1, choices=KIND_OF_EVENT_CHOICES, default='C')
	name = models.CharField(max_length=255)
	speaker = models.CharField(max_length=255, blank=True, null=True)
	company = models.CharField(max_length=255, blank=True, null=True)
	venue = models.ForeignKey(Venue)
	time = models.ManyToManyField(TimeStripe)
	description = models.TextField()
	instructions = models.TextField(blank=True, null=True)
	capacity = models.IntegerField(max_length=4, blank=True, null=True)
	slug = models.SlugField()

	def __unicode__(self):
		return "<%s: %s>" % (self.get_kind_of_event_display(), self.name)