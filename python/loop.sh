#!/bin/bash

while [ : ]
do
    clear
    python3 <YOURPATH>/python/main.py
   python3 <YOURPATH>/python/forecast.py  
  sleep 2
    echo "Sleeping..."
    sleep 300
done
