# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.messages import get_messages
from django.shortcuts import render, redirect
from .models import *
from .decorators import *


@check_if_user_has_profile
def home(request):

	context = {}
	return render(request, 'home.html', context)

@check_if_user_has_profile
def activity(request):

	context = {}
	return render(request, 'activity.html', context)

def create_profile(request):
	context = {'course_choices':COURSE_CHOICES}
	return render(request, 'create_profile.html', context)
