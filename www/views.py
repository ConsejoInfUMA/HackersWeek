from django.shortcuts import render
from django.contrib import messages
from django.contrib.messages import get_messages



def home(request):
	context = {}
	return render(request, 'home.html', context)

def activity(request):
	#messages.add_message(request, messages.DEBUG, "Horsey Bollox!")

	storage = get_messages(request)
	for message in storage:
		print message 
	context = {}
	return render(request, 'activity.html', context)
