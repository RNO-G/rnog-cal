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
