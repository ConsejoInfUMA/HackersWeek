from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
	url(r'^actividad/', views.activity, name='activity'),
    url(r'^$', views.home, name='home'),
)

