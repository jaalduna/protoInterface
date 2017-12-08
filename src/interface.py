from pylibftdi import Device

class interface(Device):
	"""docstring for interface"""
	def __init__(self, int_select):
		super(interface, self).__init__(interface_select = int_select)
		
	def reset(self):
		self.ftdi_fn.ftdi_set_bitmode(0,0)
		self.ftdi_fn.ftdi_set_bitmode(0,2) # protoInterface always reset into MPSSE mode, exept for uart mode! 
		