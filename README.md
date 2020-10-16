# rnog-cal
testing code for rno-g calibration pulse driver board

## getting started:

Turning on the Cal Driver Board: <br>
`sudo ./calBoardOn.sh` <br>
Note that `sudo` is only required for the first use after a Beaglebone restart. A green LED on the board should light up.

Turning off the Cal Driver Board:<br>
`sudo ./calBoardOff.sh`<br>
Note that `sudo` is only required for the first use after a Beaglebone restart. The green LED on the board should turn off.

See `cal_i2c.py` for example usage of the Cal Driver board

To toggle the pulse using the Beaglebone:<br>
`sudo ./enableBBBpps.sh`<br>
which will generate a repetitive digital pulse to the Cal Driver board. Note that `sudo` is only required for the first use after a Beaglebone restart.<br>
To stop, use `ctl-c`, or can run continuously in the background by running as `./enableBBBpps.sh &`
