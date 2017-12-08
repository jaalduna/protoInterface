

class gpio(object):
	"""docstring for gpio"""
	def __init__(self, interface, byte, position, direction, state):
		self.interface = interface #Device interface
		self.byte = byte #1 high byte, 0: low byte
		self.position = position # value between 0 - 7 indicating bit position
		self.direction = direction # 1 output, 0: input
		self.state = state # 1: on, 0: off
		if(byte == 1):
			self.write_opcode = 0x82
			self.read_opcode =  0x83
		else:
			self.write_opcode = 0x80
			self.read_opcode = 0x81
		self.initialize()
		



	def initialize(self):
		self.set_gpio_pin(self.state, self.direction)


	def set_value(self,value):
		#lets check we are writting on a output pin
		if(self.direction == 1):
			if(value > 0):
				self.state = 1
			else:
				self.state = 0
			self.set_gpio_pin(self.state,self.direction)

	def set_gpio_pin(self,value,direction):
		bytes = [self.write_opcode, value << self.position, direction<<self.position]
		res = "".join(map(chr, bytes))  
		self.interface.write(res)
		