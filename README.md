# rnog-cal
testing code for rno-g calibration pulse driver board

## getting started on revN: <br>
Log onto RNO-G UChicago cluster, then ssh as follows. Note that the IP address will change based on the ethernet
cord connected to the controller board. <br>
`ssh rno-g@<ip-address>` <br>
The controller board runs on 28 V. To enable pulsing on controller board, follow these steps. <br>
Command for setting cal pulse attenuation and pulse vs. sine wave is as follows: <br>
To turn cal board on:<br>
`gpioset CAL_EN=1` <br>
To enable pulse, need to turn on GPS board for PPS: <br>
`gpioset GPS_EN=1` <br>
To use GPS pulse as the trigger pulse:
`gpioset PPS_SELECT=1` <br>
IF it's the first time configuring a controller board, need to do: <br>
`ubxtool -z CFG-TP-LEN_TP1,10000,7 ::/dev/ttyGPS`

To turn the board off: <br>

To turn cal board off: <br>
`gpioset CAL_EN=0` <br>
To turn GPS board off:<br>
`gpioset GPS_EN=0` <br>

Command for setting cal pulse attenuation and pulse vs. sin wave is as follows. <br>
python3 cal_i2c_revN.py <atten> <output_ch> <wavetype>  <br>

<atten>: attenuation between [0,63] (63 is largest pulse)
<output_ch>: in range [0,3] (this refers to the SMA outputs on the pulser board)
<wavetype>: 0 (pulse) or 1 (sine wave)

## getting started on revE:

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
