from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
	url(r'^$', views.home, name='home'),
	url(r'^api/calendar/$', views.calendar, name='calendar'),
	url(r'^actividad/', views.activity, name='activity'),
    url(r'^accounts/', views.create_profile, name='create_profile'),
)

