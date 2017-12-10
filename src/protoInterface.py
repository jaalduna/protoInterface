from pylibftdi import Device
from interface import interface
from gpio import gpio


#ref: AN_108 Version 1.5
class protoInterface(object):
	"""docstring for protoInterface"""
	def __init__(self):
		#Lets define interfaces
		self.interface_a = interface(int_select = 1)
		self.interface_b = interface(int_select = 2)
	
		#lets initizlize interface A and B into mpsse mode
		self.interface_b.reset()
		self.interface_a.reset()

		#lets define gpio's
		self.led_user = gpio(self.interface_b.port_h, 7, 1, 0)
		self.gpio_1 = gpio(self.interface_a.port_l, 4, 1, 0)
		self.gpio_2 = gpio(self.interface_a.port_l, 5, 1, 0)

		self.sel_spi_jtag = gpio(self.interface_b.port_l, 4, 1, 0)
		self.sel_spi_uart = gpio(self.interface_b.port_l, 5, 1, 0)
		
