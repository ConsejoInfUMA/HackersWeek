from django.shortcuts import render

def home(request):
	context = {}
	return render(request, 'home.html', context)

def activity(request):
	context = {}
	return render(request, 'activity.html', context)
