
class port(object):
	"""docstring for port"""
	def __init__(self,dev, write_opcode, read_opcode):
		self.dev = dev
		self.write_opcode = write_opcode
		self.read_opcode = read_opcode
		self.direction = 0x00
		self.value = 0x00

		#set all pins as input.
		self.mpsse_set_data(0x00, 0x00)
		
	"""docstring for mpsse_set_data"""
	def mpsse_set_data(self, value, direction):
		bytes = [self.write_opcode, value, direction]
		res = "".join(map(chr, bytes))  
		self.dev.write(res)

	"""docstring for mpsse_set_data"""
	def mpsse_get_data(self):
		bytes = [self.read_opcode]
		res = "".join(map(chr, bytes))  
		self.dev.write(res)
		data = self.dev.read(1)
		#return self.dev.read(1)
		return data
		#return "".join(map(chr,[self.dev.read(res)]))
		



	"""docstring for set_bit_value"""
	def set_bit_value(self,pos,value):		
		if(value == 1):
			self.value |= 1 << pos
		else:
			self.value &= ~(1 << pos)

		self.mpsse_set_data(self.value, self.direction)

	"""docstring for set_bit_direction"""
	def set_bit_direction(self,pos,direction):
		if(direction == 1):
			self.direction |= 1<< pos
		else:
			self.direction &= ~(1 << pos)

		self.mpsse_set_data(self.value, self.direction)

		