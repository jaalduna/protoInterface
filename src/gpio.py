
class gpio(object):
	"""docstring for gpio"""
	def __init__(self, port, position, direction, value):
		#self.interface = interface #Device interface
		#self.byte = byte #1 high byte, 0: low byte
		self.port = port
		self.position = position # value between 0 - 7 indicating bit position
		self.direction = direction # 1 output, 0: input
		self.value = value # 1: on, 0: off
		#self.initialize()

		self.port.set_bit_value(self.position,self.value)
		self.port.set_bit_direction(self.position,self.direction)

		#flags 
		self.flag_rise = 0
		self.flag_fall = 0

	def set_value(self,value):
		self.value = value
		self.port.set_bit_value(self.position,self.value)

	def toggle_value(self):
		if(self.value == 1):
			self.value = 0
		else:
			self.value = 1
		self.port.set_bit_value(self.position,self.value)

	def set_direction(self,direction):
		self.direction = direction
		self.port.set_bit_direction(self.position,self.direction)

	def get_value(self):
		port_value = self.port.mpsse_get_data()
		port_value = int(port_value.encode('hex'),16)
		port_value &= 1<<self.position

		self.update_flags(port_value>0)
		return port_value > 0

	def update_flags(self,port_value):
		if(self.value == 0  and port_value == 1):
			self.flag_rise = 1
		elif(self.value == 1 and port_value == 0):
			self.flag_fall == 1
		else:
			self.flag_rise = 0
			self.flag_fall = 0



		



		