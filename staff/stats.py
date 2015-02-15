from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount
from www.models import *
from www.choices import * 

def get_stats():
	#Initialize stats objects
	stats = {}

	#Add user# to stats
	user_no = User.objects.all().count()
	stats.update({'user_no':user_no})
	#Facebook vs No Facebook
	face_no = SocialAccount.objects.all().filter(provider='facebook').count()
	no_face_no = user_no - face_no
	stats.update({'face_vs_noface':{'face':face_no,'no_face':no_face_no}})
	#Courses
	courses = {}
	for choice in COURSE_CHOICES:
		courses.update({choice[1]:UserProfile.objects.filter(course=choice[0]).count()})
	stats.update({'courses':courses})



	return stats