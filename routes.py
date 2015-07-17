import urllib2
import json
import time
from datetime import datetime
from time import mktime
from flask import Flask, render_template, request
import pudb

app = Flask(__name__)
app.config.from_object('config')

@app.route('/', methods=['POST', 'GET'])
def home():
	#pu.db
	#set location to nyc by default, or set location to user-entered value
	if request.method == 'GET':
		location = str(10025)
	elif request.method == 'POST':
		location = request.form['usr_zip']

	#dict with links to image files
	weather_desc = {"Clear": "../static/img/start-cycling-gl.jpg", 
					"Rain": "../static/img/rain-cycling.jpg", 
					"Clouds": "../static/img/clouds.jpg",
					"Overcast": "../static/img/overcast.png",
					"Partly Cloudy": "../static/img/partcloud.jpg",
					"Chance of a Thunderstorm": "../static/img/thunderstorm.jpg",
					"Mostly Cloudy": "../static/img/mostly-cloudy.jpg",
					"Thunderstorm": "../static/img/actual-thunderstorm.jpg"}

	#city_name = raw_input("please enter your city: ")
	#country_code = raw_input("please enter your county: ")

	#get json data from wunderground
	response = urllib2.urlopen('http://api.wunderground.com/api/4263ad1dd9572760/forecast10day/q/' + location + '.json')
	response_json = json.loads(response.read())

	#setup empty array to fill in with weather json data
	weather_list = range(0,7)
	for i in range(0,7):
		weather_list[i] = []

	#iterate over json data, and fill next seven days into weather_list array
	for i in range(0,7):
		day = response_json["forecast"]["simpleforecast"]["forecastday"][i]["date"]["weekday"]
		high = response_json["forecast"]["simpleforecast"]["forecastday"][i]["high"]["fahrenheit"]
		low = response_json["forecast"]["simpleforecast"]["forecastday"][i]["low"]["fahrenheit"]
		weather = response_json["forecast"]["simpleforecast"]["forecastday"][i]["conditions"]
		weather_pic = weather_desc[weather]
		#populate weather list with data for each day
		weather_list[i] = [day, str(high), str(low), weather, weather_pic]

	#return weather_list to home.html so that home.html can make table
	return render_template('home.html', 
							weather = weather_list,
							local = location)

@app.route('/about')
def about():
	return render_template('about.html')

if __name__ == '__main__':
	app.run(debug=True)