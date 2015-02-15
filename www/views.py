# -*- coding: utf-8 -*-
import json 

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages import get_messages
from django.http import HttpResponse
from django.shortcuts import render, redirect



from .models import *
from .decorators import *


@check_if_user_has_profile
def home(request):
	"""
	This function displays the home page
	"""
	context = {}
	return render(request, 'home.html', context)

@check_if_user_has_profile
def activity(request, slug):
	"""
	This function displays each activity page or redirect
	home if the slug is not found
	"""
	context = {}

	#TODO: enrollment logic

	if not Event.objects.filter(slug=slug).exists():
		return redirect('home')
	else:
		context.update({'event':Event.objects.get(slug=slug)})

	return render(request, 'activity.html', context)

@login_required
def profile_details(request):
	"""
	TODO: This function should display a page to create a new
	profile or edit the existing one
	"""
	context = {}
	if request.method == 'POST':
		#In order to edit the user profile details, there has to be an user xD
		fields = ['first_name','last_name', 'dni', 'course', 'email']
		if all(x in request.POST.keys() for x in fields):

			first_name = request.POST['first_name']
			last_name = request.POST['last_name']
			dni = request.POST['dni']
			email = request.POST['email']
			course = request.POST['course']

			if 'auto_enroll' in request.POST:
				auto_enroll = (request.POST['auto_enroll'] == 'True')
			else:
				auto_enroll=False


			# Get the user & user profile objects
			user = request.user
			if UserProfile.objects.filter(user=user).exists():
				user_profile = UserProfile.objects.get(user=user)
			else:
				user_profile = UserProfile(user=user)

			# Alter their fields
			user.first_name = first_name
			user.last_name = last_name
			user.email = email

			user_profile.dni = dni
			user_profile.course = course
			user_profile.auto_enroll_all = auto_enroll

			# And save them…
			user.save()
			user_profile.save()

			# Just before redirecting the user to the home page
			messages.success(request, 'Perfil actualizado correctamente.')
			return redirect('home')

		else:
			messages.error(request, 'Falta alguno de los datos.')
			return redirect('profile_details')
	else:
		# We need to display the course choices in the template
		if UserProfile.objects.filter(user=request.user).exists():
			user_profile = UserProfile.objects.get(user=request.user)
		else:
			user_profile = None

		context.update({'course_choices':COURSE_CHOICES, 
						'user_profile':user_profile})
		return render(request, 'profile_details.html', context)


def calendar(request):
	"""
	This function generates the calendar in JSON
	TODO: refactoring
	"""

	response = {}
	# Next bucle generates the response base
	# That could be cached using Django's Cache Framework
	#
	# https://docs.djangoproject.com/en/1.7/topics/cache/
	for day in DAY_CHOICES:
		response.update({day[0]:{'day_name':DAY_CHOICES_CALENDAR[day[0]-1][1], 'day_no':day[0] ,'stripes':{}}})
		for stripe in TIME_STRIPE_CHOICES:
			response[day[0]]['stripes'].update({stripe[0]:{'time':TIME_STRIPE_CALENDAR[stripe[0]-1][1],'events':{}}})
			for koe in KIND_OF_EVENT_CHOICES:
				response[day[0]]['stripes'][stripe[0]]['events'].update({koe[0]:{'kind':koe[1],'empty':True}})

	# We load the event variable with all confirmed events
	events = Event.objects.all().filter(confirmed=True)
	# And load the response with data from these events
	for event in events:
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