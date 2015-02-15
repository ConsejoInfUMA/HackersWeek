from django.shortcuts import render
from .decorators import check_is_staff
from .stats import get_stats


@check_is_staff
def staff_home(request):
	"""
	Home view for Staff
	"""
	
	context = {'stats':get_stats()}

	return render(request, 'staff_home.html', context)