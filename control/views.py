from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
def staff_required(login_url="home"):
    return user_passes_test(lambda u: u.is_staff, login_url=login_url)

@staff_required()
def control(request):

	return render(request, 'control.html', {})
