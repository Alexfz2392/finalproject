from __future__ import unicode_literals
from django.shortcuts import render, redirect
from .models import *
from datetime import date


def index(request):
	return render(request, "app/index.html")

def create(request):
	user = User.objects.register(request.POST,request)
	if user == True:
		return redirect("/user/show")

	else:
		return redirect("/")

def login(request):
	user = bool(User.objects.login(request.POST, request))
	if user == True:
		return redirect("/user/show")
	else:
		return redirect("/")

def show(request):
	user = User.objects.get(id = request.session['id'])
	yourtrips = YourTrip.objects.filter(user = user)
	yourtrips1 = YourTrip.objects.exclude(user = user)
	for i in yourtrips:
		yourtrips1 = yourtrips1.exclude(trip = i.trip)
	return render(request,"app/success.html", {"user": user, "yourtrips": yourtrips, "yourtrips1": yourtrips1})

def logout(request):
	request.session.clear()
	return redirect("/")

def trip_create(request):
	return render(request, "app/add_trip.html")

def trip_build(request):
	trip = bool(Trip.objects.build(request.POST,request))
	print trip
	if trip == True:
		return redirect("/user/show")
	else:
		return redirect("/trip/create")

def destination(request,number):
	trip = Trip.objects.get(id = number)
	user = User.objects.get(id = request.session['id'])
	groupmembers = YourTrip.objects.filter(trip__id = number).exclude(user = user)
	return render(request, "app/destination.html", {"trip": trip, "groupmembers": groupmembers})

def jointrip(request,number):
	user = User.objects.get(id = request.session['id'])
	trip = Trip.objects.get(id = number)
	YourTrip.objects.create(user = user, trip = trip)
	return redirect("/user/show")

