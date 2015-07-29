import urllib2
import json
import time
import pudb
from app import app
from datetime import datetime
from time import mktime
from flask import Flask, render_template, request, redirect, url_for, session
import os
from models import *

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
		#get form inputs
		firstname = request.form['firstname']
		lastname = request.form['lastname']
		zipcode = request.form['zipcode']
		email = request.form['email']
		password = request.form['password']
		#create new user
		new_user = User(firstname, lastname, email, password, zipcode)

		#check if email exists in db
		if new_user.check_for_duplicate_email():
			#add new user to db (function from models.py)
			new_user.add_to_db()

			#set session object to remember user email
			#session takes care of hashing email into an encrypted ID and storing it in a cookie in the user's browser
			session['email'] = new_user.email

			#return (1) signin user (2) redirect to profile
			return redirect(url_for('profile'))
		else:
			error = "A user with that email already exists"
			return render_template('signup.html',
									error = error)
		
	elif request.method == 'GET':
		return render_template('signup.html')

@app.route('/profile')
def profile():
	if 'email' not in session:
		redirect(url_for('signin'))

	user = User.lookup_email(session['email'])

	if user is None:
		return redirect(url_for(signin))
	else:
		return render_template('profile.html')

@app.route('/signin', methods=['POST', 'GET'])
def signin():
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		user = User.lookup_email(email)
		if user is None:
			error = "A user with that email address doesn't exist :("
			return render_template('signin.html',
									error = error)
		elif user.check_password(password) is False:
			error = "There was an error with ur password :("
			return render_template('signin.html',
									error = error)
		else:
			session['email'] = user.email
			return render_template('profile.html')
	elif request.method == 'GET':
		return render_template('signin.html')

@app.route('/signout')
def signout():
	if 'email' not in session:
		return redirect(url_for('signin'))

	session.pop('email', None)
	return redirect(url_for('home'))
