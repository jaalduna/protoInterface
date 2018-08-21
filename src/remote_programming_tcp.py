import socket
#import serial
import crcmod
import struct
import time

crc16 = crcmod.predefined.mkPredefinedCrcFun("modbus")

class Programmer:

	def __init__(self, file_address):
		self.TCP_IP = '192.168.0.19'
		self.TCP_PORT = 50001
		self.BUFFER_SIZE  = 256
		#lets configure socket
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.file_address = file_address
		self.incLines = 3
		print("Initializing tcp socket and file")
		self.s.connect((self.TCP_IP, self.TCP_PORT))
		self.s.settimeout(4)
		self.file = open(self.file_address, 'r')
		self.modbusSlaveId = 0x04


	def print_modbus(self,res):
		print(":".join("{:02x}".format(ord(c)) for c in res))

	def print_hex(self,value):
		print "{:01x}".format(ord(value)),

	def file_len(self):
	    with open(self.file_address) as f:
	        for i, l in enumerate(f):
	            pass
	    return i + 1

	def receive_retry(self,packet,length,verbose = False):
		while True:
			try:
				self.s.send(packet)
				data = self.s.recv(self.BUFFER_SIZE)
				if(verbose):
					self.print_modbus(data)
				if(len(data) >= length):
					print("Ok")
					return data
			except:
				print "no answer...",
				pass
	def get_version(self):
		print "Bootloader version: ",
		packet = bytearray()
		packet.append(self.modbusSlaveId) #id
		packet.append(0x04) #fcode
		packet.append(0x00) #base address h
		packet.append(0x03) #base address l
		packet.append(0x00) #num regs h
		packet.append(0x03) #num regs l

		#crc calculation
		packet += struct.pack("<H", crc16(str(packet)))
		#print_modbus(str(packet))
		data = self.receive_retry(packet, 11)

		self.print_hex(data[6])
		print ".",
		self.print_hex(data[8])
		print("")

	def enable_control_pins(self):
		print "enable control pins: ",
		packet = bytearray()
		packet.append(self.modbusSlaveId) #id
		packet.append(0x04) #fcode
		packet.append(0x00) #base address h
		packet.append(0x0a) #base address l
		packet.append(0x00) #num regs h
		packet.append(0x01) #num regs l

		#crc calculation
		packet += struct.pack("<H", crc16(str(packet)))
		#print_modbus(str(packet))

		data = self.receive_retry(packet,7)

	def erase_flash(self):
		print "Erase Flash: ",
		packet = bytearray()
		packet.append(self.modbusSlaveId) #id
		packet.append(0x04) #fcode
		packet.append(0x00) #base address h
		packet.append(0x04) #base address l
		packet.append(0x00) #num regs h
		packet.append(0x02) #num regs l

		#crc calculation
		packet += struct.pack("<H", crc16(str(packet)))
		#print_modbus(str(packet))

		self.s.send(packet)

		try:
			data = self.s.recv(self.BUFFER_SIZE)
			if(data[6] == b'\x00' and data[4] == b'\x04'):
				print "Ok"
				return True
			else:
				print "Error"
				return False
		except:
			print("no answer")
			return False
		#print_modbus(res)
	def reset_uc_to_bootloader(self):
		print "Reset to bootloader: ",
		packet = bytearray()
		packet.append(self.modbusSlaveId) #id
		packet.append(0x04) #fcode
		packet.append(0x00) #base address h
		packet.append(0x01) #base address l
		packet.append(0x00) #num regs h
		packet.append(0x01) #num regs l

		#crc calculation
		packet += struct.pack("<H", crc16(str(packet)))
		#print_modbus(str(packet))

		data = self.receive_retry(packet,7)

	def reset_uc_to_app(self):
		print "Reset to app: ",
		packet = bytearray()
		packet.append(self.modbusSlaveId) #id
		packet.append(0x04) #fcode
		packet.append(0x00) #base address h
		packet.append(0x02) #base address l
		packet.append(0x00) #num regs h
		packet.append(0x01) #num regs l

		#crc calculation
		packet += struct.pack("<H", crc16(str(packet)))
		#print_modbus(str(packet))

		data = self.receive_retry(packet,7)

	def disable_control_pins(self):
		print "disable control pins: ",
		packet = bytearray()
		packet.append(self.modbusSlaveId) #id
		packet.append(0x04) #fcode
		packet.append(0x00) #base address h|
		packet.append(0x09) #base address l
		packet.append(0x00) #num regs h
		packet.append(0x01) #num regs l

		#crc calculation
		packet += struct.pack("<H", crc16(str(packet)))
		#print_modbus(str(packet))

		data = self.receive_retry(packet,7)

	def program_record(self,record):
		l = len(record)
		# print "programming record: ",
		packet = bytearray()
		packet.append(self.modbusSlaveId)
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
		self.s.send(packet)

		try:
			data = self.s.recv(self.BUFFER_SIZE)
			if(len(data) == 7):
				print("Ok")
				return True
			return False
		except:
			print("no answer")
			return False
		# print_modbus(res)
		try:
			if(data[1] == b'\x10' and struct.unpack("B",data[5])[0] == packet[5]):
				# print "ok"
				pass
			else:
				# print "error"
				pass
		except:
			# print "error"
			pass
	def get_record(self):

		packet = bytearray()
		packet.append(0) #reserve space for num_bytes
		num_bytes = 0
		for i in range(0,self.incLines):
			line = self.file.readline()
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
	def program_file(self):

		self.enable_control_pins()
		self.reset_uc_to_bootloader()
		self.get_version()
		self.erase_flash()
		# ser.timeout = 100
		numLinesTotal = self.file_len()
		numLines = 0
		while(True):
			print "\rprogramming: {:0.1f}%".format(numLines*1.0/numLinesTotal*100),
			record = self.get_record()


			# print_modbus(str(record))
			if(len(record) == 2):
				print ""
				print "program transfer complete ;)"
				break
			self.program_record(record)
			numLines +=self.incLines

		# enable_control_pins()
		# reset_uc_to_app()
		# disable_control_pins()
		# get_value()
		self.s.close()

		#jump_to_app()





#programmer = Programmer("./test_serial.hex")
#programmer.program_file()
