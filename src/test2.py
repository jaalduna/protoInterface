file_address = "../../uc_pri/blink_led/firmware/blink_led.X/dist/default/production/blink_led.X.production.hex"
file = open(file_address, 'r')

line = file.readline()
for c in line[1:-1]: #lets skip first character
	packet.append(bytes(c,'utf-8'))
	# print(bytes(c,'utf-8'))