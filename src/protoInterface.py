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
		



		#lets initizlize interface B into mpsse mode
		self.interface_b.reset()


		#lets configure gpio related with interfaceB
		self.led_user = gpio(self.interface_b, 1, 7, 1, 0)

		
