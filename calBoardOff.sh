#!/bin/bash -e

if [ ! -d /sys/class/gpio/gpio49 ]; then echo 49 > /sys/class/gpio/export; fi

echo low > /sys/class/gpio/gpio49/direction
