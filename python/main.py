import requests
import ast
from influxdb import InfluxDBClient
import time
from datetime import datetime

current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
json_payload = []

f = open("cities.txt", "r")
lines = f.read().splitlines()  # Use this rather than readlines so we remove the newline character
f.close()

for i in range(len(lines)):
    r = requests.get(
        "https://api.openweathermap.org/data/2.5/weather?q=" + lines[i] + "&appid=<APIKEY>")

    data = r.content
    dict_str = data.decode("UTF-8")
    mydata = ast.literal_eval(dict_str)
    temp = mydata["main"]["temp"]
    temp = round(temp - 273.15,2)
    temp_max = mydata["main"]["temp_max"]
    temp_max = round(temp_max - 273.15,2)
    temp_min = mydata["main"]["temp_min"]
    temp_min = round(temp_min - 273.15,2)
    feels_like = mydata["main"]["feels_like"]
    feels_like = round(feels_like - 273.15,2)
    description = mydata["weather"][0]["main"]
    description_precise = mydata["weather"][0]["description"].capitalize()
    visibility = float(mydata["visibility"]) / 1000
    humidity = mydata["main"]["humidity"]
    sunrise = datetime.fromtimestamp(mydata["sys"]["sunrise"]).strftime('%H:%M')
    sunset = datetime.fromtimestamp(mydata["sys"]["sunset"]).strftime('%H:%M')
    wind = float(mydata["wind"]["speed"])

    data1 = {
        "measurement": "weather",
        "time": current_time,
        "tags": {
            "city": lines[i].capitalize(),
            "measures": "measured"
        },
        "fields": {
            "temp": temp,
            "temp_min": temp_min,
            "description": description_precise,
            "temp_max": temp_max,
            "humidity": humidity,
            "wind": wind,
            "sunrise": sunrise,
            "visibility": visibility,
            "sunset": sunset,
            "feels_like": feels_like
        }
    }

    json_payload.append(data1)

client = InfluxDBClient('localhost', 8086, '<ID>', '<PASSWORD>', 'weather')
client.create_database('weather')
client.write_points(json_payload)
print("Script weather finished")

