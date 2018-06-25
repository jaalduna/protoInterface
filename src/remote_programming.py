import serial
import crcmod
import struct
import time

file_address = "./test_serial.hex"

modbusSlaveId = 4;

def print_modbus(res):
	print(":".join("{:02x}".format(ord(c)) for c in res))

#ser = serial.Serial(port='COM7',baudrate=115200, timeout=1)
ser = serial.Serial(port='tty.usbserial-AI04OC5W',baudrate=115200, timeout=1)
crc16 = crcmod.predefined.mkPredefinedCrcFun("modbus")

def print_hex(value):
	print "{:01x}".format(ord(value)),

def file_len(file):
    with open(file) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def get_version():
	print "Bootloader version: ",
	packet = bytearray()
	packet.append(modbusSlaveId) #id
	packet.append(0x04) #fcode
	packet.append(0x00) #base address h
	packet.append(0x03) #base address l
	packet.append(0x00) #num regs h
	packet.append(0x03) #num regs l

	#crc calculation
	packet += struct.pack("<H", crc16(str(packet)))
	#print_modbus(str(packet))


	ser.write(packet)
	res = ser.read(11)
	while len(res) == 0:
		ser.write(packet)
		res = ser.read(11)

	#print_modbus(res)
	print_hex(res[6])
	print ".",
	print_hex(res[8])
	print ""
	
def reset_uc_to_bootloader():
	print "Reset to bootloader: ",
	packet = bytearray()
	packet.append(modbusSlaveId) #id
	packet.append(0x04) #fcode
	packet.append(0x00) #base address h
	packet.append(0x01) #base address l
	packet.append(0x00) #num regs h
	packet.append(0x01) #num regs l

	#crc calculation
	packet += struct.pack("<H", crc16(str(packet)))
	#print_modbus(str(packet))

	ser.write(packet)
	res = ser.read(7)
	if(len(res) == 7):
		print "Ok"

def reset_uc_to_app():
	print "Reset to app: ",
	packet = bytearray()
	packet.append(modbusSlaveId) #id
	packet.append(0x04) #fcode
	packet.append(0x00) #base address h
	packet.append(0x02) #base address l
	packet.append(0x00) #num regs h
	packet.append(0x01) #num regs l

	#crc calculation
	packet += struct.pack("<H", crc16(str(packet)))
	#print_modbus(str(packet))

	ser.write(packet)
	res = ser.read(7)
	if(len(res) == 7):
		print "Ok"


def enable_control_pins():
	print "enable mclr: "
	packet = bytearray()
	packet.append(modbusSlaveId) #id
	packet.append(0x04) #fcode
	packet.append(0x00) #base address h
	packet.append(0x0a) #base address l
	packet.append(0x00) #num regs h
	packet.append(0x01) #num regs l

	#crc calculation
	packet += struct.pack("<H", crc16(str(packet)))
	#print_modbus(str(packet))

	ser.write(packet)
	res = ser.read(7)
	if(len(res) == 7):
		print "Ok"	

def disable_control_pins():
	print "enable mclr: "
	packet = bytearray()
	packet.append(modbusSlaveId) #id
	packet.append(0x04) #fcode
	packet.append(0x00) #base address h
	packet.append(0x09) #base address l
	packet.append(0x00) #num regs h
	packet.append(0x01) #num regs l

	#crc calculation
	packet += struct.pack("<H", crc16(str(packet)))
	#print_modbus(str(packet))

	ser.write(packet)
	res = ser.read(7)
	if(len(res) == 7):
		print "Ok"	


def jump_to_app():
	print "Reset to bootloader: ",
	packet = bytearray()
	packet.append(modbusSlaveId) #id
	packet.append(0x04) #fcode
	packet.append(0x00) #base address h
	packet.append(0x08) #base address l
	packet.append(0x00) #num regs h
	packet.append(0x01) #num regs l

	#crc calculation
	packet += struct.pack("<H", crc16(str(packet)))
	#print_modbus(str(packet))

	ser.write(packet)
	res = ser.read(7)
	if(len(res) == 7):
		print "Ok"	
		
def erase_flash():
	print "Erase Flash: ",
	packet = bytearray()
	packet.append(modbusSlaveId) #id
	packet.append(0x04) #fcode
	packet.append(0x00) #base address h
	packet.append(0x04) #base address l
	packet.append(0x00) #num regs h
	packet.append(0x02) #num regs l

	#crc calculation
	packet += struct.pack("<H", crc16(str(packet)))
	#print_modbus(str(packet))

	ser.write(packet)
	res = ser.read(15)
	#print_modbus(res)
	
	if(res[6] == b'\x00' and res[4] == b'\x04'):
		print "Ok"
	else:
		print "Error"

def program_record(record):
	l = len(record)
	# print "programming record: ",
	packet = bytearray()
	packet.append(modbusSlaveId)
	packet.append(0x10)
	packet.append(0x00)
	packet.append(0x05) #programming record command
	packet.append(0x00)
	if(l % 2 == 0):
		packet.append(l/2)
		packet.append(l)
	else:
		packet.append((l+1)/2) # number of regs\
		packet.append(l+1)
	#for value in record:
	packet+=record
	packet += struct.pack("<H", crc16(str(packet)))
	# print packet
	# print_modbus(str(packet))
	ser.write(packet)
	res = ser.read(8)
	# print_modbus(res)
	try:
		if(res[1] == b'\x10' and struct.unpack("B",res[5])[0] == packet[5]):
			# print "ok"
			pass
		else:
			# print "error"
			pass
	except:
		# print "error"
		pass
	


def get_record(file):
	
	packet = bytearray()
	packet.append(0) #reserve space for num_bytes
	num_bytes = 0
	for i in range(0,5):
		line = file.readline()
		if(len(line) == 0):
			break
		
		num_bytes += len(line[1:-1])/2
		packet += bytearray.fromhex(line[1:-1]);

	if(num_bytes % 2 == 0):
		packet.append(0)
		num_bytes+=1
	packet[0] = num_bytes
	# for c in line[1:-1]:
	# 	print c
	# 	packet.append(c)
	# 	# packet.append(bytes(c,'utf-8'))
	# file.close()
	return packet

def get_value():
	print "get value: "
	packet = bytearray()
	packet.append(modbusSlaveId) #id
	packet.append(0x04) #fcode
	packet.append(0x00) #base address h
	packet.append(0x78) #base address l
	packet.append(0x00) #num regs h
	packet.append(0x01) #num regs l

	#crc calculation
	packet += struct.pack("<H", crc16(str(packet)))
	#print_modbus(str(packet))
	ser.flushInput()
	ser.write(packet)
	res = ser.read(7)
	if(len(res) == 7):
		print_modbus(res)

if ser.isOpen():
	#Lets ask for verison
	enable_control_pins()
	reset_uc_to_bootloader()
	get_version()
	erase_flash()
	# ser.timeout = 100
	file = open(file_address, 'r')
	numLinesTotal = file_len(file_address)
	numLines = 0
	while(True):
		print "\rprogramming: {:0.1f}%".format(numLines*1.0/numLinesTotal*100),
		record = get_record(file)


		# print_modbus(str(record))
		if(len(record) == 2):
			print ""
			print "program transfer complete ;)"
			break
		program_record(record)
		numLines +=5

	enable_control_pins()
	reset_uc_to_app()
	disable_control_pins()
	get_value()

	#jump_to_app()


	ser.close()
	file.close()


