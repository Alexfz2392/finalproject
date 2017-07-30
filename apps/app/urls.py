from django.conf.urls import url,include
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^user/create', views.create),
    url(r'^user/login', views.login),
    url(r'^user/show', views.show),
    url(r'^user/logout', views.logout),
	url(r'^trip/create', views.trip_create),
	url(r'^trip/build', views.trip_build),
	url(r'^destination/(?P<number>\d+)', views.destination),
	url(r'^trip/join/(?P<number>\d+)', views.jointrip)

 
]
