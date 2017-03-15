# StudentLocation-Receiver

A python program for tracking student primary school to fix the problem of traffic jam.

# How to setup this program?
you can setup via setup.py, get [file](https://raw.githubusercontent.com/aqover/StudentLocation-Receiver/master/setup.sh)

#Enviorment file
don't forget to create new eny.py on your machine.
```python
# for scan.py
DEBUG 				= False
DEBUG_MAC_FILTER 	= "xx:xx:xx:xx:xx:xx"

BASE_URL            = "http://xxxxx/"
MAC_ADDRESS         = "xx:xx:xx:xx:xx:xx"

# for client.py
SWING_CONSTANTS 	= 10

# for calculate distance
A_METER_SIGNAL		= -57 # signal at a meter
A_METER_CONSTANTS	= 2.0 # multiple

# use move average or kalman or both for filter rssi
FILTER_RSSI 		= 0 	# 0 - BOTH, 1 - KALMAN_FILTER, 2 - MOVING_AVERANGE

FILTER_RANGE_TYPE 	= -1 	# -1 - DISABLE, 0 - FILTER_RANGE_RSSI, 1 - FILTER_RANGE_DISTANCE
FILTER_RANGE 		= -70 	# if you use filter range by rssi this value is format dBi and if you use filter range by distance this value
							format meter.

# for moving average
MOVING_AVERAGE_CONTANCE = 0.75

# for kalman filter
PROCESS_NOISE 		= 0.008		# noise power desirable
NEASUREMENT_NOISE 	= 1.00		#
STATE_VECTOR 		= 1.00		#
CONTROL_VECTOR 		= 0.00		#
MEASUREMENT_VECTOR 	= 1.00		#

# for udp_socket.py
HOSTNAME 			= 'xxx.xxx.xxx.xxx'
PORT 				= xxx
```
