from django.conf.urls import patterns, url

from staff import views

urlpatterns = patterns('',
	url(r'^$', views.staff_home, name='staff_home'),
)

