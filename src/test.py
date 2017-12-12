import time
from protoInterface import protoInterface
from Event import Event



class ExampleOject(object):
	def __init__(self):
		self.button_pressed = Event('Button Pressed')
		self.button_released = Event('Button released')


def example_handler(*args):
	print args[0]


def button_on(*args):
	#print args[0]
	if(pi.led_user.value == 0):
		print "turning led on"
		pi.led_user.set_value(1)
	else:
		print "turning led off"
		pi.led_user.set_value(0)


pi = protoInterface()

pi.gpio_1.set_direction(1) # output for feed with 3.3V to the push button
pi.gpio_2.set_direction(0) # input for push button
pi.led_user.set_direction(1) # output to indicate when the button is pressed

pi.led_user.set_value(0)
pi.gpio_1.set_value(1)

#pi.interface_a.reset_uart()

pi.sel_spi_jtag.set_value(1)
pi.sel_spi_uart.set_value(0)
pi.interface_a.dev.baudrate = 115200

current_push = 1
previous_push = 1

ev = ExampleOject()
ev.button_pressed.add(button_on)
#ev.button_released.add(example_handler)



while(1):
	previous_push = current_push
	current_push = pi.gpio_2.get_value() 
	if(previous_push == 1 and current_push == 0):
		ev.button_pressed()		
	elif (previous_push == 0 and current_push == 1):
		ev.button_released()

	#time.sleep(0.01)





"""
dev = Device(interface_select = 2)

dev.ftdi_fn.ftdi_set_bitmode(0,0)
dev.ftdi_fn.ftdi_set_bitmode(0,2)
#byte_data = bytes(0x82 0x)
while(1):
	bytes = [0x82, 0x00, 0x80]
	res = "".join(map(chr, bytes))                                                                                          

	dev.write(res)
	time.sleep(1)
	bytes = [0x82, 0x80, 0x80]
	res = "".join(map(chr, bytes))

	dev.write(res)
	time.sleep(1)


"""
#dev.fdll.ftdi_write_data(print("%x%x%x",0x82,0x80,0x80),3)	