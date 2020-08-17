#!/bin/bash -e

if [ ! -d /sys/class/gpio/gpio47 ]; then echo 47 > /sys/class/gpio/export; fi

echo low > /sys/class/gpio/gpio47/direction

if [ ! -d /sys/class/gpio/gpio66 ]; then echo 66 > /sys/class/gpio/export; fi


while [ : ]
do

    echo high > /sys/class/gpio/gpio66/direction
    sleep 0.005s
    echo low > /sys/class/gpio/gpio66/direction
    sleep 0.2

done
    
