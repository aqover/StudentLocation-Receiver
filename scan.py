import bluetooth._bluetooth as bluez
import datetime
import json
import requests
import struct
import time
import threading

# add environment file
import env

from src.everthing import AdPayLoad, AdInfoHeader, MetaEvent, BlueZHeader
from src.clients import DeviceCliens

DEBUG = env.DEBUG

OGF_LE_CTL = 0x08
OCF_LE_SET_SCAN_ENABLE = 0x000C

BASE_URL            = env.BASE_URL
MAC_ADDRESS         = env.MAC_ADDRESS

def process_input(bluez_packet):
    bluezHeader = BlueZHeader(bluez_packet[:3])
    if bluezHeader.hci_packet_type != 0x04 or bluezHeader.event != 0x3E:
        return None, None, 0;

    metaEvent = MetaEvent(bluez_packet[3:5])
    if metaEvent.subevent != 0x02:
        return None, None, 0;

    adInfoHeader    = AdInfoHeader(bluez_packet[5:14])
    rssi            = struct.unpack('>b', bluez_packet[-1])[0]
    tx_power        = 0

    adData = []
    if adInfoHeader.lenght + 14 + 1 == len(bluez_packet):
        bluez_packet = bluez_packet[14:]
        while len(bluez_packet) > 1:
            ad_lenght = struct.unpack('<B', bluez_packet[0])[0]
            ad_type = struct.unpack('<B', bluez_packet[1])[0]
            data = bluez_packet[2: ad_lenght + 1]
            adData.append(AdPayLoad([ad_lenght, ad_type, data]))
            bluez_packet = bluez_packet[ad_lenght + 1: ]

            if ad_type == 0x0a:
                try:
                    tx_power = struct.unpack('>b', data)[0]
                except:
                    tx_power = struct.unpack('>b', data[0])[0]
            elif ad_type == 0xff:                                           # Beacon
                mfg_id_low, mfg_id_high = struct.unpack('>BB', data[0:2])
                if mfg_id_low == 0x4c and mfg_id_high == 0x00:              # iBeacon
                    tx_power = struct.unpack('>b', data[-1])[0]
    return (adInfoHeader.bdaddr, rssi, tx_power)

def send(clients):
    url = BASE_URL + 'sendLocation/' + MAC_ADDRESS

    try:
        r = requests.get(url, data=json.dumps({'data': clients}), headers={'content-type': 'application/json'})
        #if DEBUG:
            #print (r.text.encode('utf-8').strip())  
    except Exception as e:
        pass

def scan(devices):
    try:
        # Open the bluetooth device
        sock = bluez.hci_open_dev(0)
    except:
        # Failed to open
        sock = None

    if sock:
        # We have device access, start BLE scan
        cmd_pkt = struct.pack("<BB", 0x01, 0x00)
        bluez.hci_send_cmd(sock, OGF_LE_CTL, OCF_LE_SET_SCAN_ENABLE, cmd_pkt)

        time_pre = datetime.datetime.now()

        while True:
            # Save the current filter setting
            old_filter = sock.getsockopt(bluez.SOL_HCI, bluez.HCI_FILTER, 14)

            # Set filter for getting HCI events
            flt = bluez.hci_filter_new()
            bluez.hci_filter_all_events(flt)
            bluez.hci_filter_set_ptype(flt, bluez.HCI_EVENT_PKT)
            sock.setsockopt(bluez.SOL_HCI, bluez.HCI_FILTER, flt)

            # Get and decode data
            buffers = sock.recv(255)

            mac_address, rssi, tx_power = process_input(buffers)
            if mac_address != None:
                devices.append(mac_address, rssi, tx_power)

            time_now = datetime.datetime.now()
            if (time_now - time_pre).total_seconds() > 5:
                break

            #Restore the filter setting
            sock.setsockopt(bluez.SOL_HCI, bluez.HCI_FILTER, old_filter) 

        clients = devices.get_device()
        if DEBUG:
            print (clients)
        else:
            send(clients)

if __name__ == '__main__':
    DEBUG = True
    env.DEBUG = True
    devices = DeviceCliens()
    while True:
        scan(devices)  