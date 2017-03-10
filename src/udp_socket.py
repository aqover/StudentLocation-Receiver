import socket
import env

class Udp(object):
	"""docstring for Udp"""
	def __init__(self, arg):
		super(Udp, self).__init__()
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.hostname = env.HOSTNAME
		self.port = env.PORT

	def SetHost(self, host):
		self.hostname = host

	def SetPort(self, port):
		self.port = port

	def GetServer(self):
		message = 'IP=?';
		sent = self.sock.sendto(message, self._host_address())

		data, address = sock.recvfrom(1024)
		print (address, data)
		if data:
			return data

		return None

	def _host_address(self):
		return (self.hostname, self.port)
		