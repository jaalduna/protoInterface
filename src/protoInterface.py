from pylibftdi import Device
from interface import interface
from gpio import gpio


#ref: AN_108 Version 1.5
class protoInterface(object):
	"""docstring for protoInterface"""
	uart_mode = True
	def __init__(self):
		#Lets define interfaces
		self.interface_a = interface(int_select = 1)
		self.interface_b = interface(int_select = 2)
	
		#lets initizlize interface A and B into mpsse mode
		self.interface_b.reset()
		self.interface_a.reset_uart()


		#lets define gpio's
		self.led_user = gpio(self.interface_b.port_h, 7, 1, 0)

		if(self.uart_mode == False):
			self.gpio_1 = gpio(self.interface_a.port_l, 4, 1, 0)
			self.gpio_2 = gpio(self.interface_a.port_l, 5, 1, 0)

		self.gpio_mclr = gpio(self.interface_b.port_h, 0, 1, 1)
		self.gpio_boot_en = gpio(self.interface_b.port_h, 1, 1, 1)
		self.gpio_5 = gpio(self.interface_b.port_h, 2, 1, 1)
		self.gpio_6 = gpio(self.interface_b.port_h, 3, 1, 1)
		self.gpio_7 = gpio(self.interface_b.port_h, 4, 1, 1)
		self.gpio_8 = gpio(self.interface_b.port_h, 5, 1, 1)
		self.gpio_9 = gpio(self.interface_b.port_h, 6, 1, 1)

		self.sel_spi_jtag = gpio(self.interface_b.port_l, 4, 1, 0)
		self.sel_spi_uart = gpio(self.interface_b.port_l, 5, 1, 0)
		
