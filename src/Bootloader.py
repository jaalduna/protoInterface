import struct
import crcmod
import socket
import time
#AN1388 Microchip bootloader implementation

#constants declaration

##Control character description
SOH  = 0x01 #Marks the beginning of a frame
EOT = 0x04 #Marks the end of a frame
DLE = 0x10 #Data link escape

##Command description
READ_BOOTLOADER_VERSION = 0x01
ERASE_FLASH = 0x02
PROGRAM_FLASH = 0x03
READ_CRC = 0x04
JUMP_TO_APP = 0x05

crc16 = crcmod.predefined.mkPredefinedCrcFun("xmodem")

class Bootloader(object):
    """docstring for [object Object]."""
    def __init__(self):
        super(Bootloader, self).__init__()
        self.TCP_IP = '192.168.0.19'
        self.TCP_PORT = 5050
        self.BUFFER_SIZE  = 256
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # print("Initializing tcp socket and file")
        # self.socket.connect((self.TCP_IP, self.TCP_PORT))
        self.socket.settimeout(2)

    def __del__(self):
        self.socket.close()


    def read_version(self):
        packet = bytearray()
        packet.append(SOH)
        packet.append(READ_BOOTLOADER_VERSION)
        #crc calculation
        packet += struct.pack("<H", crc16(str(packet[1:len(packet)]))) # calculate CRC discarding SOH
        packet.append(EOT)
        packet = self.encode(packet)
        response = self.receive_retry(packet,7,True)
        try:
            response = self.decode(response)
            print "decoded message: ",
            self.print_modbus(str(response))
        except:
            print "error"
            time.sleep(1)


        # print "packet content: ",
        # print(":".join("{:02x}".format(ord(c)) for c in str(packet)))

    def encode(self, packet):
        #for each data byte
        result = bytearray()
        result.append(packet[0])

        for x in packet[1:len(packet) - 1]:
            if(x == DLE or x == SOH or x == EOT):
                result.append(DLE)
                result.append(x)
            else:
                result.append(x)

        result.append(packet[len(packet) - 1])
        return result
    def decode(self, packet):
        prev_is_dle = False
        #for each data byte
        result = bytearray()
        #find first SOH byte

        if(packet[0] != b'\x01'):
            print "First byte is not SOH!"
            return 0
        if(packet[len(packet) - 1 ] != b'\x04'):
            print "Last byte is not EOT"
            return 0
        for x in packet[1:len(packet) -1]:
            if(prev_is_dle):
                result.append(x)
            elif(x == b'\x10'):
                prev_is_dle = True
            else:
                prev_is_dle = False
                result.append(x)
        return result


    def receive_retry(self,packet,length,verbose = False):
        start_time = 0
        stop_time = 0
        try:
            print "connecting..."
            self.socket.connect((self.TCP_IP, self.TCP_PORT))
        except:
            print "can't connect"
            self.close_socket()
            return
        try:
            print "sending: ",
            print str(packet)
            start_time = (time.time()*1000)
            #self.print_modbus(str(packet))

            self.socket.send(packet)
            counter = 10
            data = ""
            while(counter >0):
                counter -= 1
                data += self.socket.recv(self.BUFFER_SIZE)
                # if(verbose):
                #     print data
                    #self.print_modbus(data)
                if(len(data) >= length):
                    stop_time = (time.time()*1000)
                    self.close_socket()
                    print "time elapsed: ",
                    print str(stop_time - start_time)
                    print "data received ok: ",
                    self.print_modbus(data)
                    return data
                time.sleep(0.1)
        except:
            print "no answer...",
            self.close_socket()
            dummy = bytearray()
            return dummy

    def close_socket(self):
        #lets close socket
        self.socket.close()
        #lets reasign socket so it can be opened again
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(2)
        time.sleep(0.01)
    def print_modbus(self,res):
    	print(":".join("{:02x}".format(ord(c)) for c in res))
b = Bootloader()
count = 5
while(count>0):
    count -= 1;
    b.read_version()
    #time.sleep(0)
