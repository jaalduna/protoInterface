import time
from protoInterface import protoInterface


pi = protoInterface()

while(1):
	time.sleep(1)
	pi.led_user.set_value(0)
	time.sleep(1)
	pi.led_user.set_value(1)



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