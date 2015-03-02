from django.conf.urls import patterns, url

from staff import views

urlpatterns = patterns('',
	url(r'^$', views.staff_home, name='staff_home'),
	url(r'^conferences/$', views.conferences, name='conferences'),
	url(r'^workshops/$', views.workshops, name='workshops'),
	url(r'^games/$', views.games, name='games'),
	url(r'^misc/$', views.misc, name='misc'),
	url(r'^attendance/$', views.attendance, name='attendance'),
)

