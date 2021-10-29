# Temperature_city
Script and dashboard for grafana 

## 1. Edit loop.sh

Edit temperatureloop.sh with **sudo nano loop.sh** and change /YOUR/PATH/


## 2. Edit loop.sh
Put your cities in cities.txt separated with a break line.

## 3. Edit python/main.py. 
Create an account on openweathermap.org, change <YOURCITY> with the city you want to monitor and replace <YOURAPIKEY> with your apikey.

## 4. Create a docker-compose.yml file

run

   ```shell
   user:~/appdata$ sudo docker-compose up  
   user:~/appdata$ sudo docker-compose start
   ```

  
 Copy dashboard_weather.json and dashboard_forecast.json and paste in import it in "Import via panel json" in Grafana
