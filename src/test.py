import time
from protoInterface import protoInterface


pi = protoInterface()

pi.gpio_1.set_direction(1) # output for feed with 3.3V to the push button
pi.gpio_2.set_direction(0) # input for push button
pi.led_user.set_direction(1) # output to indicate when the button is pressed

pi.led_user.set_value(0)
pi.gpio_1.set_value(0)

pi.interface_a.reset_uart()

pi.sel_spi_jtag.set_value(1)
pi.sel_spi_uart.set_value(0)
pi.interface_a.dev.baudrate = 115200

while(1):
	#if(pi.gpio_2.get_value() == 0):
	pi.led_user.toggle_value()
	pi.interface_a.dev.write('hola mundo!')
	time.sleep(0.5)



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