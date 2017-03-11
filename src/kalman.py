
class Kalman(object):
	"""docstring for Kalman"""
	def __init__(self, R = 1, Q = 1, A = 1, B = 0, C = 1):
		super(Kalman, self).__init__()
		self._process_noise 	= R # noise power desirable
		self._measurement_noise = Q
		self._state_vector 		= A
		self._control_vector 	= B
		self._measurement_vector = C

		self.cov 	= None
		self.x 		= None	# estimated signal without noise

	def filter(self, z, u = 0):
		if self.x == None:
			self.x = (1 / self._measurement_vector) * z
			self.cov = (1 / self._measurement_vector) * self._measurement_noise * (1 / self._measurement_vector)
		else:
			# Compute prediction
			predX = (self._state_vector * self.x) + (self._control_vector * u)
			predCov = ((self._state_vector * self.cov) * self._state_vector) + self._process_noise

			# Kalman gain
			K = predCov * self._measurement_vector * (1 / ((self._measurement_vector * predCov * self._measurement_vector) + self._measurement_noise))

			# Correction
			self.x = predX + K * (z - (self._measurement_vector * predX))
			self.cov = predCov - (K * self._measurement_vector * predCov)
		
		return self.x

	def lastMeasurement(self):
		return self.x

	def setMeasurement(self, noise):
		self._measurement_noise = noise

	def setProcessnoise(self, noise):
		self._process_noise = noise