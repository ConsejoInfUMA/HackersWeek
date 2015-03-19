from django.conf.urls import patterns, url

from staff import views

urlpatterns = patterns('',
	url(r'^$', views.staff_home, name='staff_home'),
	url(r'^conferences/$', views.conferences, name='conferences'),
	url(r'^workshops/$', views.workshops, name='workshops'),
	url(r'^games/$', views.games, name='games'),
	url(r'^misc/$', views.misc, name='misc'),
	url(r'^mba/$', views.mba, name='mba'),
	url(r'^facebook/$', views.facebook, name='facebook'),
	url(r'^att_stats/$', views.att_stats, name='att_stats'),	
	url(r'^attendance/$', views.attendance, name='attendance'),
	url(r'^api/lookup/$', views.busqueda, name='busqueda'),
	url(r'^attendance/(?P<event_id>\d+)/$', views.attendance_event, name='attendance_event'),
	url(r'^attendance/(?P<event_id>\d+)/e/$', views.enrol_attendance, name='enrol_attendance'),
)

