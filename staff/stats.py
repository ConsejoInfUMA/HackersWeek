from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount
from www.models import *
from www.choices import * 
from datetime import datetime, date, timedelta
from itertools import chain, combinations
from collections import defaultdict
from models import StaffDictionary

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


def get_fb_stats():

	ups = UserProfile.objects.all()
	all_users = UserProfile.objects.all().count()
	fb = SocialAccount.objects.all().filter(provider='facebook').count()
	no_fb = all_users - fb

	fb_stats = {}
	for code, name in COURSE_CHOICES:
		this_users = ups.filter(course=code)
		total_this = this_users.count()
		fb = SocialAccount.objects.all().filter(provider='facebook', user__in=[x.user for x in this_users]).count()
		no_fb = total_this - fb
		if not total_this<2:
			fb_stats.update({code:{ 'name': name,
								'no_fb':no_fb,
								'fb':fb}})
	
	print fb_stats

	return fb_stats

def apriori():
	'''
	Apriori algorithm for MBA, from https://github.com/asaini/Apriori/

	Support & Confidence can be set-up in the admin panel
	'''
	try:
		min_support = StaffDictionary.objects.get(key="min_support").value
		min_confidence = StaffDictionary.objects.get(key="min_confidence").value
	except:
		a = StaffDictionary(key='min_support', value=0.1)
		b = StaffDictionary(key='min_confidence', value=0.6)
		a.save()
		b.save()
		min_support = 0.1
		min_confidence = 0.6

	items, rules = runApriori(get_mba_sets(), 0.1, 0.8)
	return get_results(items, rules)


def get_mba_sets():
	for u in UserProfile.objects.all():
		if not u.auto_enroll_all:
			k = [u.course]
			for e in u.user.events.all():
				k.append(e.slug)
			yield frozenset(k)


def subsets(arr):
	""" Returns non empty subsets of arr"""
	return chain(*[combinations(arr, i + 1) for i, a in enumerate(arr)])


def returnItemsWithMinSupport(itemSet, transactionList, minSupport, freqSet):
		"""calculates the support for items in the itemSet and returns a subset
	   of the itemSet each of whose elements satisfies the minimum support"""
		_itemSet = set()
		localSet = defaultdict(int)

		for item in itemSet:
				for transaction in transactionList:
						if item.issubset(transaction):
								freqSet[item] += 1
								localSet[item] += 1

		for item, count in localSet.items():
				support = float(count)/len(transactionList)

				if support >= minSupport:
						_itemSet.add(item)

		return _itemSet


def joinSet(itemSet, length):
		"""Join a set with itself and returns the n-element itemsets"""
		return set([i.union(j) for i in itemSet for j in itemSet if len(i.union(j)) == length])


def getItemSetTransactionList(data_iterator):
	transactionList = list()
	itemSet = set()
	for record in data_iterator:
		transaction = frozenset(record)
		transactionList.append(transaction)
		for item in transaction:
			itemSet.add(frozenset([item]))              # Generate 1-itemSets
	return itemSet, transactionList


def runApriori(data_iter, minSupport, minConfidence):
	"""
	run the apriori algorithm. data_iter is a record iterator
	Return both:
	 - items (tuple, support)
	 - rules ((pretuple, posttuple), confidence)
	"""
	itemSet, transactionList = getItemSetTransactionList(data_iter)

	freqSet = defaultdict(int)
	largeSet = dict()
	# Global dictionary which stores (key=n-itemSets,value=support)
	# which satisfy minSupport

	assocRules = dict()
	# Dictionary which stores Association Rules

	oneCSet = returnItemsWithMinSupport(itemSet,
										transactionList,
										minSupport,
										freqSet)

	currentLSet = oneCSet
	k = 2
	while(currentLSet != set([])):
		largeSet[k-1] = currentLSet
		currentLSet = joinSet(currentLSet, k)
		currentCSet = returnItemsWithMinSupport(currentLSet,
												transactionList,
												minSupport,
												freqSet)
		currentLSet = currentCSet
		k = k + 1

	def getSupport(item):
			"""local function which Returns the support of an item"""
			return float(freqSet[item])/len(transactionList)

	toRetItems = []
	for key, value in largeSet.items():
		toRetItems.extend([(tuple(item), getSupport(item))
						   for item in value])

	toRetRules = []
	for key, value in largeSet.items()[1:]:
		for item in value:
			_subsets = map(frozenset, [x for x in subsets(item)])
			for element in _subsets:
				remain = item.difference(element)
				if len(remain) > 0:
					confidence = getSupport(item)/getSupport(element)
					if confidence >= minConfidence:
						toRetRules.append(((tuple(element), tuple(remain)),
										   confidence))
	return toRetItems, toRetRules


def get_results(items, rules):
	"""prints the generated itemsets and the confidence rules"""
	k=[]
	k.append("\n------------------------ ITEMS - support:")
	for item, support in items:
		k.append("item: %s , %.3f" % (str(item), support))
	k.append("\n------------------------ RULES - confidence:")
	for rule, confidence in rules:
		pre, post = rule
		k.append("Rule: %s ==> %s , %.3f" % (str(pre), str(post), confidence))
	return '\n'.join(k)

