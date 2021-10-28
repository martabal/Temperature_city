# Temperature_city
Script and dashboard for grafana 

## 1. Edit loop.sh

Edit temperatureloop.sh with **sudo nano loop.sh** and change /YOUR/PATH/


## 2. Edit python/main.py. 
Create an account on openweathermap.org, change <YOURCITY> with the city you want to monitor and replace <YOURAPIKEY> with your apikey.

## 3. Create a docker-compose.yml file

run

   ```shell
   user:~/appdata$ sudo docker-compose up  
   user:~/appdata$ sudo docker-compose start
   ```

  
 Login on your grafana instance and import via pannel json the content in dashboard.json
