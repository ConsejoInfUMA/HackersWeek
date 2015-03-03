from django.shortcuts import render
from .decorators import check_is_staff
from .stats import get_stats, apriori
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
	
	context = {	}

	return render(request, 'attendance.html', context)