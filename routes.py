import urllib2
import json
import time
import pudb
from datetime import datetime
from time import mktime
from flask import Flask, render_template, request, redirect, url_for
import os
import models

app = Flask(__name__)

def weather_images():
	return {"Clear": "../static/img/start-cycling-gl.jpg", 
			"Rain": "../static/img/rain-cycling.jpg", 
			"Clouds": "../static/img/clouds.jpg",
			"Overcast": "../static/img/overcast.png",
			"Partly Cloudy": "../static/img/partcloud.jpg",
			"Chance of a Thunderstorm": "../static/img/thunderstorm.jpg",
			"Mostly Cloudy": "../static/img/mostly-cloudy.jpg",
			"Thunderstorm": "../static/img/actual-thunderstorm.jpg",
			"Chance of Rain": "../static/img/pitt.jpg"}

def fetch_json(location):
	response = urllib2.urlopen('http://api.wunderground.com/api/4263ad1dd9572760/forecast10day/q/' + location + '.json')
	return json.loads(response.read())

def create_seven_day_forecast_list(response_json, weather_desc):
	#setup empty array to fill in with weather json data
	weather_list = []

	for i in range(0,7):
		day = response_json["forecast"]["simpleforecast"]["forecastday"][i]["date"]["weekday"]
		high = response_json["forecast"]["simpleforecast"]["forecastday"][i]["high"]["fahrenheit"]
		low = response_json["forecast"]["simpleforecast"]["forecastday"][i]["low"]["fahrenheit"]
		weather = response_json["forecast"]["simpleforecast"]["forecastday"][i]["conditions"]
		weather_pic = weather_desc[weather]
		#populate weather list with data for each day
		weather_list.append([day, str(high), str(low), weather, weather_pic])

	return weather_list

def create_possible_zipcode_list():
	possible_zips = range(10000, 100000)
	possible_zips = [str(num) for num in possible_zips]
	return possible_zips

def set_location_and_error(req_method, usr_zip):
	possible_zips_string = create_possible_zipcode_list()
	if req_method == 'GET':
		return {'location': str(10025), 'error': ""}
	elif req_method == 'POST':
		if usr_zip not in possible_zips_string:
			return {'location': str(10025), 'error': "That's not a valid zipcode, silly!"}
		else:
			return {'location': usr_zip, 'error': ""}

@app.route('/', methods=['POST', 'GET'])
def home():
	#get zip from form or set to empty string
	try:
		usr_zip = request.form['usr_zip']
	except:
		usr_zip = ""

	#set usr location and catch possible zipcode errors
	location_and_error_dict = set_location_and_error(request.method, usr_zip)
	location = location_and_error_dict['location']
	error = location_and_error_dict['error']

	#get image files
	weather_desc = weather_images()

	#get json data from wunderground
	response_json = fetch_json(location)

	#iterate over json data, and fill next seven days into weather_list array
	weather_list = create_seven_day_forecast_list(response_json, weather_desc)

	#return weather_list to home.html so that home.html can make table
	return render_template('home.html', 
							weather = weather_list,
							local = location,
							error = error)

@app.route('/radar', methods=['POST', 'GET'])
def radar():
	try:
		usr_zip = request.form['usr_zip']
	except:
		usr_zip = ""

	#set usr location and catch possible zipcode errors
	location_and_error_dict = set_location_and_error(request.method, usr_zip)
	location = location_and_error_dict['location']
	error = location_and_error_dict['error']

	return render_template('radar.html',
							local = location,
							error = error)

@app.route('/signup', methods=['POST', 'GET'])
def signup():
	if request.method == 'POST':
		zip_code = request.form['usr_zip']
		email = request.form['email']
		models.insert_email_and_zip(zip_code, email)
		return redirect(url_for('home'))

	return render_template('signup.html')

if __name__ == '__main__':
	app.run(debug=True)

from config import *
db.create_all()