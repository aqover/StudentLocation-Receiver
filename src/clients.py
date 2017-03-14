import datetime
import math

from src.kalman import Kalman

import env

def calculate_distance(rssi, tx_power = 0):
    signal_strnght_1_meter = env.A_METER_SIGNAL if tx_power == 0 else tx_power
    return 10.0 ** ((signal_strnght_1_meter - rssi)/(10.0 * env.A_METER_CONSTANTS))

def moving_average(rssi, rssi_prev):
    return (env.MOVING_AVERAGE_CONTANCE * rssi) + ((1.0 - env.MOVING_AVERAGE_CONTANCE)*rssi_prev)

class DeviceCliens(object):
    """docstring for DeviceCliens"""
    def __init__(self):
        super(DeviceCliens, self).__init__()
        self.device = {}

    def append(self, mac_address, rssi, tx_power):
        index = self._getIndex(mac_address)
        if index not in self.device:
            if env.FILTER_RSSI == 0:
                pass
            elif env.FILTER_RSSI == 1:
                kalman = Kalman(env.PROCESS_NOISE, env.NEASUREMENT_NOISE, env.STATE_VECTOR, env.CONTROL_VECTOR, env.MEASUREMENT_VECTOR)
                kalman.filter(rssi, 0)
                self.device[index] = [mac_address, tx_power, kalman, datetime.datetime.now()]
            elif env.FILTER_RSSI == 2:
                self.device[index] = [mac_address, tx_power, m_v.moving_average(rssi, 0), datetime.datetime.now()]            
        else:
            if (datetime.datetime.now() - self.device[index][3]).total_seconds > 0.2:
                self.device[index][3] = datetime.datetime.now()
                if env.FILTER_RSSI == 0:
                    pass
                elif env.FILTER_RSSI == 1:
                    self.device[index][2].filter(rssi, 0)
                elif env.FILTER_RSSI == 2:
                    self.device[index][2] = m_v.moving_average(rssi, self.device[index][2])

    def get_device(self):
        output = []
        time = datetime.datetime.now()
        
        ck = 1
        while ck:
            ck = 0
            for x, y in self.device.iteritems():
                if (time - y[3]).total_seconds() > 10:
                    self.device.pop(x)
                    ck = 1
                    break;

                if env.DEBUG and y[0] == "FF:FF:40:00:15:0D":
                    print ({'device_mac_address': y[0], 'signal_strength': int(y[2].lastMeasurement()), 'length': calculate_distance(y[2].lastMeasurement(), y[1])})

                if env.FILTER_RSSI == 0:
                    pass
                elif env.FILTER_RSSI == 1:
                    output.append({'device_mac_address': y[0], 'signal_strength': int(y[2].lastMeasurement()), 'length': calculate_distance(y[2].lastMeasurement(), y[1])})
                elif env.FILTER_RSSI == 2:
                    output.append({'device_mac_address': y[0], 'signal_strength': int(y[2]), 'length': calculate_distance(y[2], y[1])})

        return (output)
    
    def _getIndex(self, address):
        i = 1; sums = 0;
        
        for x in address.split(':'):
            sums = sums + (int(x, 16) * (3**i))
            i = i+1

        return (sums)