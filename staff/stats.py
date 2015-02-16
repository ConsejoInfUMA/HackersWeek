from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount
from www.models import *
from www.choices import * 
from datetime import datetime, date, timedelta



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

	# Signups per day
	open_date = date(2015, 2, 13)
	current_date = datetime.today().date()

	delta = current_date - open_date

	signups_per_day = {'labels':[],'data':[]}

	for i in range(delta.days + 1):
		analysis_date = open_date + timedelta(days=i)
		analysis_data = User.objects.filter(	date_joined__day=analysis_date.day,
									date_joined__month=analysis_date.month,
									date_joined__year=analysis_date.year).count()
		signups_per_day['labels'].append(analysis_date.strftime('%d/%b'))
		signups_per_day['data'].append(analysis_data)

	stats.update({'signups_per_day':signups_per_day})
 
	return stats