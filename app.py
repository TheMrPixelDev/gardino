"""
Gardino is a simple webapplication that stores weather data collected by mulitiple microcontrollers.
Its also capable of visualizing a dashboard for controlling 433 Mhz plugs when used on a Raspberry Pi.
"""

from flask import Flask, render_template, request, url_for, redirect, send_file
import datetime
from database import database
#import transmitter
from logger import log

app = Flask(__name__)
log_file = log('log.csv')
weather_file = log('weather.csv')
weather_database = database('weather_database.db')

@app.route('/')
def index():
    past_log_data = log_file.read_limited(5)
    past_log_data.sort(reverse=True)
    weather_data = weather_database.read_one('weather_data','temp, humid, time, date')
    return render_template("index.html", log_data=past_log_data, current_weather_data=weather_data)

@app.route('/disable/<device_id>', methods=["POST"])
def disable_device(device_id):
    log_text = "Turned off device {device}".format(device=device_id)
    log_file.append(log_text)
    print('Turning off ', device_id)

    #transmitter.turn_off(device_id)

    return redirect(url_for('index'))

@app.route('/enable/<device_id>', methods=["POST"])
def enable_device(device_id):
    log_text = f"Turned on device {device_id}"
    log_file.append(log_text)
    print('Turning on ', device_id)

    #transmitter.turn_on(device_id)

    return redirect(url_for('index'))
"""
This creates a route for the download-btn in the view.
It returns the downloadable file of the querylog.
"""
@app.route('/download/querylog')
def download_query_log():
    return send_file('log.csv')


"""Route for the button that triggers the download for the csv-file containing all the
recorded weather-data"""
@app.route('/download/weather_csv')
def download_weather_file():


    data_array = weather_database.read('weather_data','date,time,temp,humid') #reads the sql-database
    weather_file.write_array(data_array) #stores the just rode data of the sql database in an csv-file

    return send_file("weather.csv")

"""
Route that handles the incoming data from the ESP8266 aka it's postrequest
"""
@app.route('/receive/weather', methods=["POST"])
def handle_weather_data():

    if request.method == "POST":
        weather_data = request.get_json()
        date = datetime.date.today() #gets the current date
        time = str(datetime.datetime.now().time().replace(microsecond=0)) #gets the current time (HH:MM:SS)

        """
        Triggers an sql execution of an insertion in the 
        sql-database via an instance of the database-class
        """
        weather_database.write('weather_data', 'date, time, temp, humid, id', [date, time, weather_data.get('temp'), weather_data.get('humid'), weather_data.get('station_id')])

        """
        returns wether the request of the microcontroller was successful
        """
        return "success"
    else:
        return "You used the wrong request-type."

"""Route for the weather-dasboard"""
@app.route('/weather')
def weather_dashboard():

    date_today = datetime.date.today() #Get the current date
    weather_data_array = weather_database.read_conditional('date,time,temp,humid', f'date="{date_today}"') #Gets the weather data of the current day out of the sql database
    current_weather_data = weather_database.read_one('weather_data', 'temp, humid, time, date') #gets the most recent weather entry out of the database

    return render_template('weather.html', last_weather_log=current_weather_data, weather_data_array=weather_data_array)
