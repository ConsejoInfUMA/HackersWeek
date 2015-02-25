from django.shortcuts import render
from .decorators import check_is_staff
from .stats import get_stats
from www.models import *


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
def attendance(request):
	"""
	Attendance monitoring
	"""
	
	context = {	}

	return render(request, 'attendance.html', context)