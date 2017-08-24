# -*- coding: utf-8 -*-
import json 

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages import get_messages
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render, redirect



from .models import *
from .decorators import *

from staff.models import *


@check_if_user_has_profile
def home(request):
	"""
	Home page
	"""
	context = {}
	streaming_code = None
	if StaffDictionary.objects.filter(key='streaming_code').exists():
		stored_code = StaffDictionary.objects.get(key='streaming_code').value
		if not stored_code == '':
			streaming_code = stored_code
		context = { 'streaming_code':streaming_code }

	if request.user.is_staff:
		context.update({'trollimage': request.user.username})
		messages.info(request, 'Puedes <a href="/staff/">acceder aquí</a> al área de Staff.')

	
	return render(request, 'home.html', context)

@check_if_user_has_profile
def activity(request, slug):
	"""
	This function displays each activity page or redirect
	home if the slug is not found
	"""
	context = {}

	if not Event.objects.filter(slug=slug).exists():
		return redirect('home')
	else:

		event = Event.objects.get(slug=slug)

		# Not confirmed events are only visible to staff
		if not event.confirmed and not request.user.is_staff:
			return redirect('home')

		# Here we choose button destination/messages
		if request.user.is_authenticated():
			if event in request.user.events.all():
				enroll_btn = {	'class':'inscribed',
								'link':''.join(['/actividad/',event.slug,'/eliminar-inscripcion/']),
								'message':'Correctamente inscrito' }
			else:
				if event.enrollment_available():
					enroll_btn = {	'class':'',
									'link':''.join(['/actividad/',event.slug,'/inscribir/']),
									'message':'Inscribir a la actividad' }
				else:
					enroll_btn = {	'class':'',
									'link':'',
									'message':'Cupo completo' }
		else:
			enroll_btn = {	'class':'',
							'link':''.join([reverse('account_login'),'?next=', request.path]),
							'message':'Accede para inscribirte' }

		context.update({'event':event, 
						'enroll_btn':enroll_btn})

	return render(request, 'activity.html', context)

def enroll_in_activity(request, slug):
	"""
	Enrolls an user in a given activity
	"""
	if not Event.objects.filter(slug=slug).exists():
		return redirect('home')
	else:
		event = Event.objects.get(slug=slug)
		if not request.user.is_authenticated():
			messages.error(request, ''.join(['Debes acceder para inscribirte a ', event.name ,'.']))
		else:
			if event.enroll_user(request.user):
				messages.success(request, ''.join(['Correctamente inscrito a ', event.name ,'.']))
			else:
				messages.error(request, 'Ha habido un error con la inscripción, inténtalo de nuevo.')

		return redirect(reverse('activity', args=[slug]))

def kick_from_activity(request, slug):
	"""
	'Kicks' an user from a given activity
	"""
	if not Event.objects.filter(slug=slug).exists():
		return redirect('home')
	else:
		if request.user.is_authenticated():
			event = Event.objects.get(slug=slug)
			event.kick_user(request.user)
			#No messages here
		return redirect(reverse('activity', args=[slug]))

def profile_details(request):
	"""
	TODO: This function should display a page to create a new
	profile or edit the existing one
	"""

	if not request.user.is_authenticated():
		return redirect('home')

	context = {}

	next = None

	if request.method == 'POST':

		if 'next' in request.POST:
			next = request.POST['next']

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

			# Afterwards, we enroll in all conferences if decided

			if auto_enroll:
				conferences = Event.objects.filter(kind_of_event='A')
				for conference in conferences:
					conference.enroll_user(user)

			# Just before redirecting the user to the home page
			messages.success(request, 'Perfil actualizado correctamente.')
			if next:
				return redirect(next)
			else:
				return redirect('home')
			
		else:
			messages.error(request, 'Falta alguno de los datos.')
			return redirect('profile_details')
	else:
		# We find next var in request.GET
		if 'next' in request.GET:
			next = request.GET['next']

		context.update({'next':next})

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

	# We load the user events (if authenticated)
	if request.user.is_authenticated():
		user_events = request.user.events.all()
	else:
		user_events = []

	# And load the response with data from these events
	for event in events:
		event_object = {'name':event.name,
						'enr':event in user_events,
						'url':"/".join(['/actividad',event.slug,'']),
						'empty':False
						}
		for time in event.time.all():
			response[time.day]['stripes'][time.time_stripe]['events'][event.kind_of_event].update(event_object)
			# TODO: next 2 ifs (in www.views.calendar) are hardcoded, find solution
			if time.duration == 2:
				response[time.day]['stripes'][time.time_stripe+1]['events'][event.kind_of_event].update(event_object)
			if time.duration == 3:
				response[time.day]['stripes'][time.time_stripe+1]['events'][event.kind_of_event].update(event_object)
				response[time.day]['stripes'][time.time_stripe+2]['events'][event.kind_of_event].update(event_object)

	
	return HttpResponse(json.dumps(response), content_type="application/json")

def sitemap(request):

	sitemap = ['<?xml version="1.0" encoding="UTF-8"?>',
	'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">',
	'<url><loc>http://www.hackersweek.com/</loc><changefreq>weekly</changefreq><priority>1.00</priority></url>',
	'<url><loc>http://www.hackersweek.com/accounts/login/</loc><changefreq>weekly</changefreq><priority>0.80</priority></url>']

	for e in Event.objects.all().filter(confirmed=True):
		sitemap.append('<url><loc>http://www.hackersweek.com/actividad/' +e.slug+ '/</loc><changefreq>weekly</changefreq><priority>0.90</priority></url>')

	sitemap.append('</urlset>')
	return HttpResponse('\n'.join(sitemap), content_type="text/xml; charset=utf-8")

