#!/bin/bash -e

if [ ! -d /sys/class/gpio/gpio49 ]; then 
  echo 49 > /sys/class/gpio/export; 
  sleep 0.1
fi

echo high > /sys/class/gpio/gpio49/direction
