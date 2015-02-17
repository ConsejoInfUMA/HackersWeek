from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount
from www.models import *
from www.choices import * 
from datetime import datetime, date, timedelta

from google_analytics import get_google_analytics_data


# Day where Analytics should start
# TODO: use persistence (for the future)
START_ANALYTICS_DAY = date(2015, 2, 13)

def get_signups_per_day():
	"""
	Gets the number of user signups per day
	"""
	signups_per_day = {'labels':[],'data':[]}
	open_date = START_ANALYTICS_DAY
	current_date = datetime.today().date()

	delta = current_date - open_date


	for i in range(delta.days + 1):
		analysis_date = open_date + timedelta(days=i)
		analysis_date_plus_1 = analysis_date + timedelta(days=1)
		analysis_data = User.objects.filter(date_joined__range=[analysis_date,analysis_date_plus_1]).count()
		signups_per_day['labels'].append(analysis_date.strftime('%d/%b/%Y'))
		signups_per_day['data'].append(analysis_data)

	return signups_per_day

def get_stats():
	# Initialize stats objects
	stats = {}

	# Add user# to stats
	user_no = User.objects.all().count()
	stats.update({'user_no':user_no})
	# Facebook vs No Facebook
	face_no = SocialAccount.objects.all().filter(provider='facebook').count()
	no_face_no = user_no - face_no
	stats.update({'face_vs_noface':{'face':face_no,'no_face':no_face_no}})
	# Courses
	courses = {}
	for choice in COURSE_CHOICES:
		courses.update({choice[1]:UserProfile.objects.filter(course=choice[0]).count()})
	stats.update({'courses':courses})


	

	stats.update({'signups_per_day':get_signups_per_day(),'google_analytics':get_google_analytics_data()})
 
	return stats