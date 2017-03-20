import os
import time

import scan
from src.udp_socket import Udp
from src.clients import DeviceCliens

class BLE(object):
	"""docstring for BLE"""
	def __init__(self, hci = 0):
		super(BLE, self).__init__()
		self.hci = hci
		self.mac_address = ''
		self.status = 0

		os.system("sudo hciconfig hci" + str(hci) + " > /var/tmp/locating")

		fd = open("/var/tmp/locating", 'r')
		lines = fd.readlines()
		fd.close()

		if len(lines) > 5:
			self.mac_address = lines[1].split()[2]
			self.status = (lines[2].strip() == "UP RUNNING")
		os.system("rm /var/tmp/locating")

	def GetMac_address(self):
		return self.mac_address

	def GetStatus(self):
		os.system("sudo hciconfig hci" + str(self.hci) + " > /var/tmp/locating")

		fd = open("/var/tmp/locating", 'r')
		lines = fd.readlines()
		fd.close()

		if len(lines) > 5:
			self.status = (lines[2].strip() == "UP RUNNING")
		else:
			self.status = False
		os.system("rm /var/tmp/locating")

		return self.status
		

if __name__ == '__main__':
	time.sleep(10)

	device = BLE(0)

	print (device.GetMac_address())
	print (device.GetStatus())

	if device.GetMac_address() != '':
		scan.MAC_ADDRESS = device.GetMac_address()
	try:
		ip = Udp().GetServer()
		if ip != None:
			scan.BASE_URL = ip
			print (ip)
	except:
		pass
	
	devices = DeviceCliens()
	while True:
		scan.scan(devices)