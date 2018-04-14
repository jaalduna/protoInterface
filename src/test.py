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
	print (args[0])


def button_on(*args):
	#print args[0]
	if(pi.led_user.value == 0):
		print ("turning led on")
		pi.led_user.set_value(1)
	else:
		print ("turning led off")
		pi.led_user.set_value(0)

def read_answer():
	time.sleep(0.03)
	res = pi.interface_a.dev.read(15)
	for c in res:
		print("0x{:02x} ".format(c),end="")
	print("")
	# print(":".join("{:02x}".format(ord(c)) for c in res))


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


pi.gpio_mclr.set_value(1)
pi.gpio_boot_en.set_value(0)

#lets force bootloader start
pi.gpio_mclr.set_value(1)
pi.gpio_boot_en.set_value(1)
time.sleep(0.1)
pi.gpio_mclr.set_value(0)
time.sleep(0.1)
pi.gpio_mclr.set_value(1)
time.sleep(0.1)
pi.gpio_boot_en.set_value(0)


pi.interface_a.dev.baudrate = 115200
print (pi.interface_a.dev.device_index)
current_push = 1
previous_push = 1
time.sleep(0.1)
# ev = ExampleOject()
# ev.button_pressed.add(button_on)
#ev.button_released.add(example_handler)


crc16 = crcmod.predefined.mkPredefinedCrcFun("xmodem")


#lets start reset sequence
# pi.gpio_mclr.set_value(0)
# pi.gpio_mclr.set_value(1)

# #lets ask for bootloader version
print("lets ask for bootloader version...")
pi.interface_a.dev.write(b'\x01\x10\x01\x21\x10\x10\x04')
# pi.interface_a.dev.write(b'\x01')
# time.sleep(0.05)
# res = pi.interface_a.dev.read(15)
# print(res)
# print(":".join("{:02x}".format(ord(c)) for c in res))
read_answer()
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
read_answer()


#lets write a hex record
print("")
print("lets write an hex record...")
##Lets open the file to be programmed
file_address = "../../uc_pri/blink_led/firmware/blink_led.X/dist/default/production/blink_led.X.production.hex"
file = open(file_address, 'r')
line = file.readline()
i = 0;
while(len(line)>0):
	packet = bytearray()
	crc_packet = bytearray()
	packet.append(0x01)
	packet.append(0x03)
	crc_packet.append(0x03)
	for j in range(1,15):
	##lets start the bytearray involved with CRC bytes 
		_bytes = bytearray.fromhex(line[1:-1])
		for c in _bytes: #lets skip first character (:) and last one ('\n')
			if(c == 0x10 or c == 0x01 or c == 0x04):
				packet.append(0x10)
			packet.append(c)
			crc_packet.append(c)
		line = file.readline()
		i += 1			
	#crc checksum is calculated over the command plus data bytes. 
	## lets calculate crc for data bytes (including)
	crc_value = crc16(crc_packet)

	#lets append crc_values to packet, but first lets transform into two integers
	crc_value_l = crc_value & 0x00ff
	crc_value_h = (crc_value >> 8) & 0x00ff
	if(crc_value_l == 0x10 or crc_value_l == 0x01 or crc_value_l == 0x04):
		packet.append(0x10)
	packet.append(crc_value_l)

	if(crc_value_h == 0x10 or crc_value_h == 0x01 or crc_value == 0x04):
		packet.append(0x10)
	packet.append(crc_value_h)

	# if(crc_value & 0x00ff == 0x10)
	# # packet.append(crc_value & 0x00ff) #low side first
	# # packet.append(crc_value>>8 & 0x00ff) #high side then.
	# packet += struct.pack("<H", crc16(crc_packet))
	# print(struct.pack("<H", crc16(crc_packet)),end="")
	#lets append end of packet command
	packet.append(0x04)

#lets send the 
	pi.interface_a.dev.write(packet)
#lets prepare to receive answer
	print("{0}: ".format(i),end="")
	read_answer()


#lets jump to the program
print("")
print("lets jump to the program...")


#lets ask for crc to check hex record was written correctly.
#remember to take into consideration the program offset in the address
# print("")
# print("lets read crc...")
# packet = bytearray()
# crc_packet = bytearray()
# packet.append(0x01)
# packet.append(0x10)
# packet.append(0x04)
# crc_packet.append(0x04)

# ADRS_LB = 0x00
# ADRS_HB = 0x00
# ADRS_UB = 0x00
# ADRS_MB = 0x00

# NUMBYTES_LB = 0x00
# NUMBYTES_HB = 0x00
# NUMBYTES_UB = 0x00
# NUMBYTES_MB = 0x00

#packet lets write
# select CRC-16-DNP

# test
# result =crc16(b'\x01')
# print (struct.pack('>H',result).encode('hex'))

# print(":".join("{:02x}".format(ord(c)) for c in res))



packet = bytearray()
crc_packet = bytearray()
packet.append(0x01)
packet.append(0x05)
crc_packet.append(0x05)
crc_value = crc16(crc_packet)
packet += struct.pack("<H", crc16(crc_packet))
packet.append(0x04)
pi.interface_a.dev.write(packet)

print("")
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
