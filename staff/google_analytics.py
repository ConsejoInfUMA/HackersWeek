# Google Analytics Imports
# -*- coding: utf-8 -*-
import os, threading, json, argparse, httplib2

from models import StaffDictionary
from oauth2client.client import Credentials 
from apiclient.discovery import build
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run_flow
from oauth2client.client import Storage as BaseStorage
from django.core.exceptions import *
from apiclient.errors import HttpError
from oauth2client.client import AccessTokenRefreshError

from datetime import datetime

class Flags():
	logging_level = 'ERROR'
	auth_host_name = 'localhost'
	noauth_local_webserver = True
	auth_host_port = [8080,8081]


HACKERS_PROFILE_ID = '79336340'

class SelfStorage(BaseStorage):
	"""Store and retrieve a single credential to and from a the database."""

	def __init__(self):
		self._lock = threading.Lock()


	def acquire_lock(self):
		"""Acquires any lock necessary to access this Storage.
		This lock is not reentrant.
		"""
		self._lock.acquire()

	def release_lock(self):
		"""Release the Storage lock.
		Trying to release a lock that isn't held will result in a
		RuntimeError.
		"""
		self._lock.release()

	def locked_get(self):
		credentials = None
		try:
			content = StaffDictionary.objects.get(key="ga_credentials").value
		except Exception:
			return credentials

		try:
			credentials = Credentials.new_from_json(content)
			credentials.set_store(self)
		except ValueError:
			pass

		return credentials

	def locked_put(self, credentials):
		if StaffDictionary.objects.filter(key="ga_credentials").exists():
			ga_credentials = StaffDictionary.objects.get(key="ga_credentials")
			ga_credentials.value = credentials.to_json()
		else:
			ga_credentials = StaffDictionary(key="ga_credentials", value=credentials.to_json())
			
		ga_credentials.save()


	
def set_credentials():
	# Retrieve existing credendials
	storage = SelfStorage()
	credentials = storage.get()
	
	if credentials is None or credentials.invalid:
		if StaffDictionary.objects.filter(key="ga_client_secrets").exists():
			ga_client_secrets = StaffDictionary.objects.get(key="ga_client_secrets").value
			#ga_client_secrets = StaffDictionary.objects.get(key="ga_client_secrets")["value"]
			client_info = json.loads(ga_client_secrets)
			scope='https://www.googleapis.com/auth/analytics.readonly'
			constructor_kwargs = {
					'redirect_uri': None,
					'auth_uri': client_info['auth_uri'],
					'token_uri': client_info['token_uri'],
					'login_hint': None,
			}
			flow = OAuth2WebServerFlow(client_info['client_id'], client_info['client_secret'],scope, **constructor_kwargs)
			flags = Flags()
			credentials = run_flow(flow, storage, flags)


	return credentials

def get_credentials():
	# Retrieve existing credendials
	storage = SelfStorage()
	credentials = storage.get()
	return credentials


def initialize_service():
	# 1. Create an http object
	http = httplib2.Http()
	# 2. Authorize the http object
	# In this tutorial we first try to retrieve stored credentials. If
	# none are found then run the Auth Flow. This is handled by the
	# prepare_credentials() function defined earlier in the tutorial
	credentials = get_credentials()
	http = credentials.authorize(http)  # authorize the http object
	# 3. Build the Analytics Service Object with the authorized http object
	return build('analytics', 'v3', http=http)


def get_google_analytics_data():
	"""
	Get analytics from Google Analytics
	"""
	reply = None

	# Get Google Analytics secrets from the database, if they exist
	if StaffDictionary.objects.filter(key="ga_client_secrets").exists():
		service = initialize_service()

		try:
			sessions_and_users = get_sessions_and_users(service, HACKERS_PROFILE_ID)

			sessions_list = []
			users_list = [] 
			for data in sessions_and_users['rows']:
				(day,month,year,sessions,users) = data
				sessions_list.append(sessions)
				users_list.append(users)
			reply = {'sessions':sessions_list, 'users':users_list}

		except TypeError, error:
			pass
		except HttpError, error:
			pass
		except AccessTokenRefreshError:
			pass

	return reply

def get_sessions_and_users(service, profile_id):
	return service.data().ga().get(
	ids='ga:' + HACKERS_PROFILE_ID,
	start_date='2015-02-23',
	end_date='today',
	sort='ga:year,ga:month,ga:day',
	metrics='ga:sessions,ga:users',
	dimensions='ga:day,ga:month,ga:year', #ga:year
	max_results='365').execute()
