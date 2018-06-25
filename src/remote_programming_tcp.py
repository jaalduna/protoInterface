import socket
import serial
import crcmod
import struct

crc16 = crcmod.predefined.mkPredefinedCrcFun("modbus")


TCP_IP = '192.168.1.62'
TCP_PORT = 5050
BUFFER_SIZE = 1024


packet = bytearray()
packet.append(0x04) #id
packet.append(0x04) #fcode
packet.append(0x00) #base address h
packet.append(0x03) #base address l
packet.append(0x00) #num regs h
packet.append(0x03) #num regs l

#crc calculation
crc = struct.pack("<H", crc16(packet))
packet += crc


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(packet)
#data = s.recv(BUFFER_SIZE)

s.close()

print("received data:")
#print(str(data))