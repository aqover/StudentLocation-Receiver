#!/usr/bin/python
# -*- mode: python; coding: utf-8 -*-

# Copyright (C) 2014, Oscar Acena <oscaracena@gmail.com>
# This software is under the terms of GPLv3 or later.

from __future__ import print_function

import sys
from time import sleep
from bluetooth.ble import GATTRequester

GATT_CHR_PROP_BROADCAST             = 0x01
GATT_CHR_PROP_READ                  = 0x02
GATT_CHR_PROP_WRITE_WITHOUT_RESP    = 0x04
GATT_CHR_PROP_WRITE                 = 0x08
GATT_CHR_PROP_NOTIFY                = 0x10
GATT_CHR_PROP_INDICATE              = 0x20
GATT_CHR_PROP_AUTH                  = 0x40
GATT_CHR_PROP_EXT_PROP              = 0x80

class Requester(GATTRequester):
    def on_notification(self, handle, data):
        print("test - notification on handle: {}\n".format(handle))

class Reader(object):
    def __init__(self, address):
        self.requester = Requester(address, False)
        self.connect()
        sleep(0.5) # Time in seconds.
        self.request_data()
        self.write_data(11)

    def connect(self):
        print("Connecting...", end=' ')
        sys.stdout.flush()

        while not self.requester.is_connected():
            try:
                self.requester.connect(True)
            except:
                print ("Error", end=' ')
                sleep(0.5) # Time in seconds.
        
        print("OK!")

    def request_data(self):     
        ck = 1
        while ck:
            try:
                ck = 0   
                data = self.requester.discover_primary()
                for x in data:
                    print (x)

                    ch = 1
                    while ch:
                        try:
                            ch = 0
                            y = self.requester.discover_characteristics(x['start'], x['end'])
                            for z in y:
                                print (z['handle'], z['value_handle'], z['uuid'], self.print_properties(z['properties']))
                        except RuntimeError as e:
                            print (e)
                            sleep(0.5) # Time in seconds.

                print ("-----------------------")
                data = self.requester.read_by_handle(3)[0]
                try:
                    print("Device name: " + data.decode("utf-8"))
                except AttributeError:
                    print("Device name: " + data)
            except RuntimeError as e:
                print (e)
                sleep(0.5) # Time in seconds.

    def write_data(self, handle):
        self.requester.write_by_handle(handle, str(1))

    def print_properties(self, prop_value):
        out = ''
        if prop_value & GATT_CHR_PROP_BROADCAST:
            out = out + 'Broadcase, '
        if prop_value & GATT_CHR_PROP_READ:
            out = out + 'Read, '
        if prop_value & GATT_CHR_PROP_WRITE_WITHOUT_RESP:
            out = out + 'Write without response, '
        if prop_value & GATT_CHR_PROP_WRITE:
            out = out + 'Write, '
        if prop_value & GATT_CHR_PROP_NOTIFY:
            out = out + 'Notify, '
        if prop_value & GATT_CHR_PROP_INDICATE:
            out = out + 'Indicate, '
        if prop_value & GATT_CHR_PROP_AUTH:
            out = out + 'Authenticated Signed Writes, '
        if prop_value & GATT_CHR_PROP_EXT_PROP:
            out = out + 'Extended Properties, '

        return out


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: {} <addr>".format(sys.argv[0]))
        sys.exit(1)

    Reader(sys.argv[1])
    print("Done.")