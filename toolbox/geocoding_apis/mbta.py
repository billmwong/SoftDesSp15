"""
Geocoding and Web APIs Project Toolbox exercise

Find the MBTA stops closest to a given location.

Full instructions are at:
https://sites.google.com/site/sd15spring/home/project-toolbox/geocoding-and-web-apis

@author: Bill Wong
"""

import urllib2, json, urllib
from pprint import pprint

def placetoURL(place):
	"""
	Returns a properly-formatted URL to make a Google maps
	geocode request of that place
	
	place: name or address of location
	returns: string of the URL
	"""
	place = place.replace(' ','+')	# replace the spaces with '+'
	return "https://maps.googleapis.com/maps/api/geocode/json?address=" + place

def getJSON(url):
	"""
	Given a properly-formatted URL for a JSON API request, returns
	a JSON object of the response to the request

	url: the formatted URL for the API request
	returns: a JSON object of the response
	"""
	f = urllib2.urlopen(url)
	text = f.read()
	return json.loads(text)

def getLatLong(place):
	"""
	Returns the latitude and longitude of a given place

	place: name or address of a place
	returns: a list of the latitude and longitude formatted [lat,long]
	"""
	url = placetoURL(place)
	json = getJSON(url)
	lat = json['results'][0]['geometry']['location']['lat']
	lon = json['results'][0]['geometry']['location']['lng']
	return [lat,lon]

def getClosestMBTA(latlng):
	"""
	Returns the nearest MBTA stop to a given latitude and longitude

	latlng: latitude and longitude in [lat,lng] format
	returns: A list of the format [name,distance]
	"""
	baseurl = 'http://realtime.mbta.com/developer/api/v2/stopsbylocation?api_key=wX9NwuHnZU2ToO7GmGR9uw'
	lat = str(latlng[0])
	lng = str(latlng[1])
	url = baseurl+'&lat='+lat+'&lon='+lng+'&format=json'

	json = getJSON(url)
	name = json['stop'][0]['stop_name']
	dist = json['stop'][0]['distance']
	return [name,dist]

def getStopNear(place):
	"""
	Prints the nearest MBTA stop and its distance away from a given
	location

	place: name or address of some place
	returns: none
	"""
	latlng = getLatLong(place)
	info = getClosestMBTA(latlng)
	print 'Nearest MBTA stop: ' + info[0]
	print 'Distance away: ' + info[1] + ' miles'

getStopNear('Fenway Park')