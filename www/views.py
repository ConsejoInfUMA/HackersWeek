from django.shortcuts import render
from django.contrib import messages
from django.contrib.messages import get_messages



def home(request):
	context = {}
	return render(request, 'home.html', context)

def activity(request):
	context = {}
	return render(request, 'activity.html', context)

def create_profile(request):
	context = {}
	return render(request, 'create_profile.html', context)
