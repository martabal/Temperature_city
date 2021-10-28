import requests
import ast
from influxdb import InfluxDBClient
import time
from datetime import datetime

current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

json_payload = []

cities = {

    0 : {
        "lat" : <LAT>,
        "lon" : <LON>,
        "name" : <NAME>
    },
    1 : {
        "lat" : <LAT>,
        "lon" : <LON>,
        "name" : <NAME>
        }
}



for j in range(len(cities)):
    r = requests.get("https://api.openweathermap.org/data/2.5/onecall?lat="+ str(cities[j]["lat"])+"&lon="+str(cities[j]["lon"])+"&appid=<APIKEY>")
    data = r.content
    dict_str = data.decode("UTF-8")
    mydata = ast.literal_eval(dict_str)

    for i in range(47):
        temp = mydata["hourly"][i]["temp"]
        temp = round(temp - 273.15, 2)
        feels_like = mydata["hourly"][i]["feels_like"]
        feels_like = round(feels_like - 273.15, 2)
        visibility = float(mydata["hourly"][i]["visibility"]) / 1000
        humidity = mydata["hourly"][i]["humidity"]
        uvi = float(mydata["hourly"][i]["uvi"])
        pop = float(mydata["hourly"][i]["pop"]) * 100
        wind = float(mydata["hourly"][i]["wind_speed"])
        time2 = mydata["hourly"][i]["dt"]
        time = (datetime.fromtimestamp(float(mydata["hourly"][i]["dt"]) - 100000 )  ).strftime('%Y-%m-%dT%H:%M:%SZ')
        time3 = (datetime.fromtimestamp(mydata["hourly"][i]["dt"])   ).strftime('%Y-%m-%dT%H:%M:%SZ')


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
                "visibility": visibility,
                "uvi": uvi,
                "pop": pop,
                "feels_like": feels_like
            }
        }

        json_payload.append(data1)


client = InfluxDBClient('localhost', 8086, '<ID>', '<PASSWORD>', 'weather')
client.create_database('weather')
client.drop_measurement('forecast')
client.write_points(json_payload)
print("Script forecast finished")

