from __future__ import unicode_literals
from django.db import models
from django.contrib import messages
import datetime
import re

class UserManager(models.Manager):
	def register(self,postData,request):

		flag = True
		#name validation 

		if len(User.objects.filter(username = postData['username'])) > 0:
			messages.add_message(request, messages.INFO, 'Your username is already registered')
			flag = False

		else:

			if len(postData['name']) < 0:

				messages.add_message(request, messages.INFO, 'You must enter a Name')
				flag = False

			elif len(postData['name']) < 3: 
				messages.add_message(request, messages.INFO, 'Your Name must be at least 3 characters')
				flag = False

			if not postData['name'].isalpha:
				messages.add_message(request, messages.INFO, 'Your Name may only contain letters')
				flag = False

			#alias validation 

			if len(postData['username']) < 0:
				messages.add_message(request, messages.INFO, 'You must enter a User Name')
				flag = False

			elif len(postData['username']) < 3: 
				messages.add_message(request, messages.INFO, 'Your User Name must be at least 3 characters')
				flag = False

			if not postData['username'].isalpha:
				messages.add_message(request, messages.INFO, 'Your User Name may only contain letters')
				flag = False


			# password validation

			if len(postData['password']) < 8:
				messages.add_message(request, messages.INFO, 'Your password must be at least 8 characters')
				flag = False

			if postData['password'] != postData['password_confirm']:
				messages.add_message(request, messages.INFO, 'Your passwords do not match')
				flag = False

		# flag check

		if flag == True:
			User.objects.create(name = postData['name'], username = postData['username'], password = postData['password'])
			request.session['id'] = User.objects.get(username = postData['username']).id
			return True

		else: 
			return False 


	def login(self, postData, request):
		user =  User.objects.filter(username = postData['username'])
		if user:
			if user[0].password == postData['password']:
				request.session['id'] = User.objects.get(username = postData['username']).id
				return True
			else:
				messages.add_message(request, messages.INFO, 'Password does not match')
				return False

		else:
			messages.add_message(request, messages.INFO, 'User Name does not exist')
			return  False

class TripManager(models.Manager):
	def build(self,postData,request):

		flag = True

		if len(postData['travel_date_from']) == 0:
			messages.add_message(request, messages.INFO, 'Opps you forgot to enter a date for departure')
			flag = False

		if len(postData['travel_date_to']) == 0:
			messages.add_message(request, messages.INFO, 'Opps you forgot to enter a Date for return')
			flag = False


		travel_date_from = datetime.datetime.strptime(postData['travel_date_from'], '%Y-%m-%d')
		travel_date_to = datetime.datetime.strptime(postData['travel_date_to'], '%Y-%m-%d')

		if travel_date_from < datetime.datetime.now():
			messages.add_message(request, messages.INFO, 'Your trip depature date must be in the future')
			flag = False

		if travel_date_to < datetime.datetime.now():
			messages.add_message(request, messages.INFO, 'Your trip return date must be in the future')
			flag = False

		if travel_date_from > travel_date_to:
			messages.add_message(request, messages.INFO, 'Your trip start date must be prior to your end date')
			flag = False
		
		if len(postData['destination']) < 1:
			messages.add_message(request, messages.INFO, 'No empty entries')
			return False

		if len(postData['description']) < 1:
			messages.add_message(request, messages.INFO, 'No empty entries')
			return False

		if len(postData['travel_date_from']) < 1:
			messages.add_message(request, messages.INFO, 'No empty entries')
			return False

		if len(postData['travel_date_to']) < 1:
			messages.add_message(request, messages.INFO, 'No empty entries')
			return False


		if flag == True:
			user = User.objects.get(id = request.session['id'])
			Trip.objects.create(user = user,destination = postData['destination'],travel_date_from = postData['travel_date_from'], travel_date_to = postData['travel_date_to'],plan = postData['description'])
			
			trip = Trip.objects.last()
			YourTrip.objects.create(user = user, trip = trip)
			return True

		else: 
			return False 

		


class User(models.Model):
	name = models.CharField(max_length = 255)
	username = models.CharField(max_length = 255)
	password = models.CharField(max_length = 255)
	created_at = models.DateTimeField(auto_now = True)
	updated_at = models.DateTimeField(auto_now_add = True)
	objects = UserManager()

class Trip(models.Model):
	user = models.ForeignKey(User, related_name = "trip_goer")
	destination = models.CharField(max_length = 255)
	travel_date_from = models.DateField()
	travel_date_to = models.DateField()
	plan = models.CharField(max_length = 255)
	created_at = models.DateTimeField(auto_now = True)
	updated_at = models.DateTimeField(auto_now_add = True)
	objects = TripManager()

class YourTrip(models.Model):
	user = models.ForeignKey(User, related_name = "users_trip")
	trip = models.ForeignKey(Trip, related_name = "trip_object")
	created_at = models.DateTimeField(auto_now = True)
	updated_at = models.DateTimeField(auto_now_add = True)
