from pylibftdi import Device
from port import port

class interface(object):
	"""docstring for interface"""
	def __init__(self, int_select):
		self.dev = Device(mode='b', interface_select = int_select, auto_detach=False, device_id = 'Dual RS232-HS' )

		self.write_port_l = 0x80
		self.read_port_l = 0x81
		self.write_port_h = 0x82
		self.read_port_h = 0x83
		self.port_l = port(self.dev,self.write_port_l, self.read_port_l)
		self.port_h = port(self.dev,self.write_port_h, self.read_port_h)	

		
	def reset(self):
		self.dev.ftdi_fn.ftdi_set_bitmode(0,0)
		self.dev.ftdi_fn.ftdi_set_bitmode(0,2) #protoInterface always reset into MPSSE mode, except for uart mode! 

	def reset_uart(self):
		self.dev.ftdi_fn.ftdi_set_bitmode(0,0)
		
