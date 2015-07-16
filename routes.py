import urllib
import json
import time
from datetime import datetime
from time import mktime
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
	def k_to_f(temp):
		return (temp - 273.15) * 1.8 + 32

	#list of days to help with day variable in table
	days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
	
	#dict with links to image files
	weather_desc = {"Clear": "../static/img/start-cycling-gl.jpg", "Rain": "../static/img/rain-cycling.jpg", "Clouds": "../static/img/clouds.jpg"}

	#city_name = raw_input("please enter your city: ")
	#country_code = raw_input("please enter your county: ")

	#get json data from openweathermap
	response = urllib.urlopen('http://api.openweathermap.org/data/2.5/forecast/daily?q={New York},{USA}&cnt={7}.json')
	response_json = json.loads(response.read())

	#setup empty array to fill in with weather json data
	weather_list = range(0,7)
	for i in range(0,7):
		weather_list[i] = []

	#iterate over json data, and fill next seven days into weather_list array
	for i in range(0,7):
		today_time = response_json['list'][i]['dt']
		day = time.localtime(today_time)[6]
		high = int(k_to_f(response_json['list'][i]['temp']['day']))
		low = int(k_to_f(response_json['list'][i]['temp']['min']))
		weather = response_json['list'][i]['weather'][0]['main']
		weather_pic = weather_desc[weather]
		#populate weather list with data for each day
		weather_list[i] = [days[day], str(high), str(low), weather, weather_pic]

	#return weather_list to home.html so that home.html can make table
	return render_template('home.html', 
							weather = weather_list)

@app.route('/about')
def about():
	return render_template('about.html')

if __name__ == '__main__':
	app.run(debug=True)