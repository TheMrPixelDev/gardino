from flask import Flask, render_template, request, url_for, redirect, send_file
import datetime
import sqlite3
#import transmitter
from logger import log

app = Flask(__name__)
log_file = log("log.csv")

@app.route('/')
def index():
    past_log_data = log_file.read_limited(5)
    past_log_data.sort(reverse=True)
    return render_template("index.html", data=past_log_data)

@app.route('/disable/<device_id>', methods=["POST"])
def disable_device(device_id):
    log_text = "Turned off device {device}".format(device=device_id)
    log_file.append(log_text)
    print('Turning off ', device_id)

    #transmitter.turn_off(device_id)

    return redirect(url_for('index'))

@app.route('/enable/<device_id>', methods=["POST"])
def enable_device(device_id):
    log_text = "Turned on device {device}".format(device=device_id)
    log_file.append(log_text)
    print('Turning on ', device_id)

    #transmitter.turn_on(device_id)

    return redirect(url_for('index'))

@app.route('/download/querylog')
def download_query_log():
    return send_file('log.csv')

@app.route('/receive/weather', methods=["POST"])
def handle_weather_data():
    if request.method == "POST":
        weather_data = request.get_json()
        date = datetime.date.today()
        time = str(datetime.datetime.now().time().replace(microsecond=0))
        params = [date, time ,weather_data.get('temp'),weather_data.get('humid'), weather_data.get('station_id')]
        print(params)
        connection = sqlite3.connect("weather_database.db")
        cursor = connection.cursor()
        cursor.execute('INSERT INTO weather_data (date, time,temp, humid, station_id) VALUES (?,?,?,?,?)', params)
        connection.commit()
        connection.close()
        return "success"
    else:
        return "You used the wrong request-type."

@app.route('/weather')
def weather_dashboard():

    connection = sqlite3.connect("weather_database.db")
    cursor = connection.cursor()
    datum = datetime.date.today()
    cursor.execute(f"SELECT date,time,temp,humid FROM weather_data WHERE date='{datum}' ORDER BY time DESC")
    daten = cursor.fetchone()
    datenliste = cursor.fetchall()
    return render_template('weather.html', daten=daten, datenliste=datenliste)
