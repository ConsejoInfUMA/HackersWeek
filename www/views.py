# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib import messages
from django.contrib.messages import get_messages
from .models import *



def home(request):
	if request.user.is_authenticated:
		pass
		#need to try

	context = {}
	return render(request, 'home.html', context)

def activity(request):
	if request.user.is_authenticated:
		pass
		#need to try
	context = {}
	return render(request, 'activity.html', context)

def create_profile(request):
	context = {'course_choices':COURSE_CHOICES}
	return render(request, 'create_profile.html', context)
