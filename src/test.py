import time
from protoInterface import protoInterface
from Event import Event
import crcmod
from pylibftdi import driver
import struct


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
time.sleep(0.1)
# pi.gpio_1.set_direction(1) # output for feed with 3.3V to the push button
# pi.gpio_2.set_direction(0) # input for push button
pi.led_user.set_direction(1) # output to indicate when the button is pressed

pi.led_user.set_value(0)
# pi.gpio_1.set_value(1)

# pi.interface_a.reset_uart()
pi.sel_spi_jtag.set_value(1)
pi.sel_spi_uart.set_value(0)
pi.interface_a.dev.baudrate = 115200
print pi.interface_a.dev.device_index
current_push = 1
previous_push = 1
time.sleep(0.1)
# ev = ExampleOject()
# ev.button_pressed.add(button_on)
#ev.button_released.add(example_handler)


crc16 = crcmod.predefined.mkPredefinedCrcFun("xmodem")


# #lets ask for bootloader version
print("lets ask for bootloader version...")
pi.interface_a.dev.write(b'\x01\x10\x01\x21\x10\x10\x04')
# pi.interface_a.dev.write(b'\x01')
time.sleep(0.05)
res = pi.interface_a.dev.read(15)
print(":".join("{:02x}".format(ord(c)) for c in res))

print("")

#lets erase flash
print("lets erase flash ...")
packet = bytearray()
packet.append(0x01)
packet.append(0x02)
# packet.append(0x42)
# packet.append(0x20)
packet += struct.pack("<H", crc16(b'\x02'))
packet.append(0x04)

pi.interface_a.dev.write(packet)
time.sleep(0.05)
res = pi.interface_a.dev.read(15)
print(":".join("{:02x}".format(ord(c)) for c in res))

print("")
print("lets write a program to flash...")
packet = bytearray()
packet.append(0x01)
packet.append(0x03)

# select CRC-16-DNP

# test
# result =crc16(b'\x01')
# print (struct.pack('>H',result).encode('hex'))

# print(":".join("{:02x}".format(ord(c)) for c in res))


print("finishing test")



# while(1):
# 	previous_push = current_push
# 	current_push = pi.gpio_2.get_value() 
# 	if(previous_push == 1 and current_push == 0):
# 		ev.button_pressed()		
# 	elif (previous_push == 0 and current_push == 1):
# 		ev.button_released()


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