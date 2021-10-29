import requests
import ast
from influxdb import InfluxDBClient
from datetime import datetime
from geopy.geocoders import Nominatim

cities = {}
json_payload = []

f = open("cities.txt", "r")
lines = f.read().splitlines()  # Use this rather than readlines so we remove the newline character
f.close()

for i in range(len(lines)):
    address = lines[i]
    geolocator = Nominatim(user_agent="Your_Name")
    location = geolocator.geocode(address)
    test = {
        "lat": location.latitude,
        "lon": location.longitude,
        "name": lines[i].capitalize()
    }
    cities[i] = test

json_payload = []

for j in range(len(cities)):
    r = requests.get("https://api.openweathermap.org/data/2.5/onecall?lat=" + str(cities[j]["lat"]) + "&lon=" + str(
        cities[j]["lon"]) + "&appid=<YOURAPIKEY>")
    data = r.content
    dict_str = data.decode("UTF-8")
    mydata = ast.literal_eval(dict_str)

    for i in range(47):
        temp = mydata["hourly"][i]["temp"]
        temp = round(temp - 273.15, 2)
        feels_like = mydata["hourly"][i]["feels_like"]
        feels_like = round(feels_like - 273.15, 2)
        humidity = mydata["hourly"][i]["humidity"]
        uvi = float(mydata["hourly"][i]["uvi"])
        pop = float(mydata["hourly"][i]["pop"]) * 100
        wind = float(mydata["hourly"][i]["wind_speed"])
        time2 = mydata["hourly"][i]["dt"]
        time = (datetime.fromtimestamp(float(mydata["hourly"][i]["dt"]) - 100000)).strftime('%Y-%m-%dT%H:%M:%SZ')
        time3 = (datetime.fromtimestamp(mydata["hourly"][i]["dt"])).strftime('%Y-%m-%dT%H:%M:%SZ')
        clouds = mydata["hourly"][i]["clouds"]
        data1 = {
            "measurement": "forecast",
            "time": time3,
            "tags": {
                "city": cities[j]["name"]
            },
            "fields": {
                "temp": temp,
                "humidity": humidity,
                "wind": wind,
                "uvi": uvi,
                "pop": pop,
                "feels_like": feels_like,
                "clouds": clouds
            }
        }

        json_payload.append(data1)

client = InfluxDBClient('localhost', 8086, '<YOURID>', '<YOURPASSWORD>', 'weather')
client.create_database('weather')
client.drop_measurement('forecast')
client.write_points(json_payload)
print("Script forecast finished")
