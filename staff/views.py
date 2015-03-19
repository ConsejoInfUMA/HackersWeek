import json

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Q
from .decorators import check_is_staff
from .stats import get_stats, get_fb_stats, apriori
from www.models import *
from .models import *
from django.http import HttpResponse

@check_is_staff
def staff_home(request):
	"""
	Home view for Staff
	"""
	
	context = {	'stats':get_stats(),
				'conferences':Event.objects.filter(kind_of_event='A'),
				'workshops':Event.objects.filter(kind_of_event='B')}

	return render(request, 'staff_home.html', context)

@check_is_staff
def facebook(request):
	"""
	Facebook Stats view
	"""
	context = {'fb_stats':get_fb_stats()}

	return render(request, 'facebook.html', context)

@check_is_staff
def conferences(request):
	"""
	Conference Stats view
	"""
	context = {'events':Event.objects.filter(kind_of_event='A')}

	return render(request, 'conferences.html', context)

@check_is_staff
def workshops(request):
	"""
	Workshop Stats view
	"""
	context = {'events':Event.objects.filter(kind_of_event='B')}

	return render(request, 'workshops.html', context)

@check_is_staff
def games(request):
	"""
	Games Stats view
	"""
	context = {'events':Event.objects.filter(kind_of_event='C')}

	return render(request, 'games.html', context)

@check_is_staff
def misc(request):
	"""
	Misc Stats view
	"""
	context = {'events':Event.objects.filter(kind_of_event='D')}

	return render(request, 'misc.html', context)

@check_is_staff
def mba(request):
	"""
	Market Basket Analysis view
	"""
	context = {'mba':apriori()}

	return render(request, 'mba.html', context)


@check_is_staff
def attendance(request):
	"""
	Attendance monitoring
	"""
	
	context = {	'events':Event.objects.all().order_by('kind_of_event') }

	return render(request, 'attendance.html', context)

@check_is_staff
def attendance_event(request, event_id):
	"""
	Attendance monitoring - Event
	"""

	event = get_object_or_404(Event, id=event_id)
	attendance = Attendance.objects.filter(event=event)
	
	context = {	'event':event, 
				'attendance':attendance }

	return render(request, 'attendance_reg.html', context)


@check_is_staff
def att_stats(request):
	"""
	Attendance Stats view
	"""
	events = []
	expected = []
	attended = []




	for e in sorted(Event.objects.all(), key= lambda t: t.enrolled_no(), reverse=True):
		events.append(e.slug)
		expected.append(e.enrolled_no())
		attended.append(e.attended_no())

	context = {
		'events':events,
		'expected':expected,
		'attended':attended,
	}

	return render(request, 'attendance_stats.html', context)

# Attendance monitoring
def busqueda(req):
	"""
	Returns a list of users that matches the search criteria
	"""
	status_code = 403
	response = []
	if req.user.is_staff:
		status_code = 200
		if 's' in req.GET and req.GET['s']!='':
			s = req.GET['s']

			query = Q()
			for term in s.split():
				query = query & Q((Q(dni__istartswith=term)|
					Q(user__username__icontains=term)|
					Q(user__first_name__icontains=term)|
					Q(user__last_name__icontains=term)|
					Q(user__email__icontains=term)))

			response = [{'name' : u.user.get_full_name(), 'username' : u.user.username,'id': u.user.id, 'hasdni': u.dni!=''} for u in UserProfile.objects.filter(query)[:4]]

	return HttpResponse(json.dumps(response), content_type="application/json", status=status_code)

def enrol_attendance(req, event_id):
	status_code = 403
	response = []
	if req.user.is_staff:
		if req.method == 'POST' and 'user_id' in req.POST:
			if not Event.objects.filter(id=event_id).exists():
				status_code = 404
			else:
				user_id = req.POST['user_id']
				if not Attendance.objects.filter(user=user_id, event=event_id).exists():
					a = Attendance(user=User.objects.get(id=user_id), event=Event.objects.get(id=event_id), scored_by=req.user)
					a.save()
					status_code = 201
					response={	'timestamp':a.timestamp.strftime('%d/%m, %H:%M'), 
								'uid':a.user.id,
								'attendees':Attendance.objects.filter(event=event_id).count(),
								'was_enrolled':a.was_enrolled()}
					print response
				else:
					status_code = 200
					response={	'uid':user_id,
								'attendees':Attendance.objects.filter(event=event_id).count(),
								'was_enrolled':False}
		else:
			status_code = 400

	return HttpResponse(json.dumps(response), content_type="application/json", status=status_code)