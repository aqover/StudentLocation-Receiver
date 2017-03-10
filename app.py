import os

import scan
from src.udp_socket import Upd

class BLE(object):
	"""docstring for BLE"""
	def __init__(self, hci = 0):
		super(BLE, self).__init__()
		self.hci = hci
		self.mac_address = ''
		self.status = 0

		os.system("sudo hciconfig hci" + str(hci) + " > tmp")

		fd = open("tmp", 'r')
		lines = fd.readlines()
		fd.close()

		self.mac_address = lines[1].split()[2]
		self.status = (lines[2].strip() == "UP RUNNING")
		os.system("rm tmp")

		if self.status == 0:
			self.Start()

	def GetMac_address(self):
		return self.mac_address

	def GetStatus(self):
		os.system("sudo hciconfig hci" + str(self.hci) + " > tmp")

		fd = open("tmp", 'r')
		lines = fd.readlines()
		fd.close()

		self.status = (lines[2].strip() == "UP RUNNING")
		os.system("rm tmp")

		return self.status

	def Start(self):
		#Can't down device hci0: Permission denied (13)
		os.system("sudo hciconfig hci" + str(self.hci) + " up")

	def Stop(self):
		os.system("sudo hciconfig hci" + str(self.hci) + " down")

	def Restart(self):
		self.Stop()
		self.Start()
		

if __name__ == '__main__':
	device = BLE(0)

	print (device.GetMac_address())
	print (device.GetStatus())

	scan.MAC_ADDRESS = device.GetMac_address()
	try:
		ip = Udp().GetServer()
		if ip != None:
			scan.BASE_URL = ip
	except:
		pass
	scan.scan()