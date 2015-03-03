from django.conf.urls import patterns, url

from . import views
from django.shortcuts import redirect

urlpatterns = patterns('',
	url(r'^$', views.home, name='home'),
	url(r'^sitemap.xml$', views.sitemap, name='sitemap'),
	url(r'^api/calendar/$', views.calendar, name='calendar'),
	#url(r'^actividad/', views.activity, name='activity'),
	url(r'^actividad/(?P<slug>[-\w\d]+)/inscribir/', views.enroll_in_activity, name='enroll_in_activity'),
	url(r'^actividad/(?P<slug>[-\w\d]+)/eliminar-inscripcion/', views.kick_from_activity, name='kick_from_activity'),
	url(r'^actividad/(?P<slug>[-\w\d]+)/', views.activity, name='activity'),
	url(r'^actividad/', lambda x: redirect('home')),
    url(r'^accounts/', views.profile_details, name='profile_details'),
)

