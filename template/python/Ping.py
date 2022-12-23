import numpy as np

class Ping:

	def __init__(self):
		self._telegramType = None
		self._messageLength = None
		self._message = None

	@property
	def telegramType(self):
		return self._telegramType

	@telegramType.setter
	def telegramType(self,value):
		self._telegramType = np.uint8(value)

	@property
	def messageLength(self):
		return self._messageLength

	@messageLength.setter
	def messageLength(self,value):
		self._messageLength = np.uint16(value)

	@property
	def message(self):
		return self._message

	@message.setter
	def message(self,value):
		self._message = str(value)

