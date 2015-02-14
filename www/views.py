# -*- coding: utf-8 -*-
import json 

from django.contrib import messages
from django.contrib.messages import get_messages
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .models import *
from .decorators import *


#@check_if_user_has_profile
def home(request):
	"""
	This function displays the home page
	"""
	context = {}
	return render(request, 'home.html', context)

#@check_if_user_has_profile
def activity(request, slug):
	"""
	This function displays each activity page or redirect
	home if the slug is not found
	"""
	context = {}

	if not Event.objects.filter(slug=slug).exists():
		return redirect('home')
	else:
		context.update({'event':Event.objects.get(slug=slug)})

	return render(request, 'activity.html', context)

def create_profile(request):
	"""
	TODO: This function should display a page to create a new
	profile (if the user is logged in and doesn't have one)
	"""
	context = {'course_choices':COURSE_CHOICES}
	return render(request, 'create_profile.html', context)


def calendar(request):
	"""
	This function generates the calendar in JSON
	TODO: refactoring
	"""
	response = {}
	for day in DAY_CHOICES:
		response.update({day[0]:{'day_name':DAY_CHOICES_CALENDAR[day[0]-1][1], 'day_no':day[0] ,'stripes':{}}})
		for stripe in TIME_STRIPE_CHOICES:
			response[day[0]]['stripes'].update({stripe[0]:{'time':TIME_STRIPE_CALENDAR[stripe[0]-1][1],'events':{}}})
			for koe in KIND_OF_EVENT_CHOICES:
				response[day[0]]['stripes'][stripe[0]]['events'].update({koe[0]:{'kind':koe[1],'empty':True}})


	for event in Event.objects.all():
		event_object = {'name':event.name,
						'enr':True, # TODO: implement user enrolled in www.views.calendar
						'url':"/".join(['/actividad',event.slug,'']),
						'empty':False
						}
		for time in event.time.all():
			response[time.day]['stripes'][time.time_stripe]['events'][event.kind_of_event].update(event_object)
			if time.duration == 2:
				# TODO: events duration in www.views.calendar is hardcoded, find solution
				response[time.day]['stripes'][time.time_stripe+1]['events'][event.kind_of_event].update(event_object)

	
	return HttpResponse(json.dumps(response), content_type="application/json")