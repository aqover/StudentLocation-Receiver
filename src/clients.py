import datetime
import math

from src.kalman import Kalman

def calculate_distance(rssi, tx_power = 0):
    signal_strnght_1_meter = -57 if tx_power == 0 else tx_power
    multiple_1_meter       = 2.0
    return 10.0 ** ((signal_strnght_1_meter - rssi)/(10.0*multiple_1_meter))

class DeviceCliens(object):
    rssi_smooth_contance = 0.5

    """docstring for DeviceCliens"""
    def __init__(self):
        super(DeviceCliens, self).__init__()
        self.device = {}

    def append(self, mac_address, rssi, tx_power):
        index = self._getIndex(mac_address)
        if index not in self.device:
            kalman = Kalman(0.008, 1.00, 1.0, 0, 1.0)
            kalman.filter(rssi, 0)
            self.device[index] = [mac_address, tx_power, kalman, datetime.datetime.now()]
        else:
            if (datetime.datetime.now() - self.device[index][3]).total_seconds > 0.2:
                self.device[index][2].filter(rssi, 0)
                self.device[index][3] = datetime.datetime.now()


        """
        if index not in self.device:
            self.device[index] = [mac_address, tx_power, [[rssi*-1, datetime.datetime.now()]], datetime.datetime.now()]
        else:
            self.device[index][2].append([rssi*-1, datetime.datetime.now()])
            #self.device[index][1] = [[rssi*-1, datetime.datetime.now()]]
            self.device[index][3] = datetime.datetime.now()
        """
            

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

                output.append({'device_mac_address': y[0], 'signal_strength': int(y[2].lastMeasurement()), 'lenght': calculate_distance(y[2].lastMeasurement(), y[1])})

                """
                if (time - y[3]).total_seconds() > 10:
                    self.device.pop(x)
                    ck = 1
                    break;

                rssi = {}; k = 0
                for n in range(len(y[2])):
                    if (time - y[2][n-k][1]).total_seconds() > 4:
                        self.device[x][2].pop(n-k)
                        k += 1
                        continue;

                    rssi[y[2][n-k][0]] = rssi[y[2][n-k][0]] + 1 if y[2][n-k][0] in rssi else 1

                maxs = 0; key = -1
                for k in rssi:
                    if rssi[k] > maxs:
                        maxs = rssi[k]; key = k
                
                output.append({'device_mac_address': y[0], 'signal_strength': key*-1, 'lenght': calculate_distance(key*-1, y[1])})
                """

        return (output)
    
    def _getIndex(self, address):
        i = 1; sums = 0;
        
        for x in address.split(':'):
            sums = sums + (int(x, 16) * (3**i))
            i = i+1

        return (sums)

    def _rssi_filter(self, rssi, rssi_prev):
        return (self.rssi_smooth_contance * rssi) + ((1.0 - self.rssi_smooth_contance)*rssi_prev)


class Cliens(object):
    """docstring for Cliens"""
    def __init__(self, bdaddr, rssi, tx_power):
        super(Cliens, self).__init__()
        self.mac_address    = bdaddr
        self.rssi           = rssi
        self.tx_power       = tx_power
        #self.distance      = distance

    def __str__(self):
        return self.mac_address + ' : ' + str(self.rssi) + ' : ' + str(self.tx_power)