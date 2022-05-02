import serial

def main():
	ser = serial.Serial(port = 'COM3', 
					baudrate=19200,
					parity=serial.PARITY_NONE, 
					stopbits=serial.STOPBITS_ONE,
					bytesize=serial.EIGHTBITS, 
					timeout=0)

	if ser.isOpen():
		print("port is open")
		
	rcvData = ser.readline(10).decode('utf_8') 				 # receive data
	ser.write(b"\xff\x00")                                       		 # send data
	print("--- Received Data ---")
	print("Data: ", rcvData)
	print("Data type: ", type(rcvData))
	print("Data length: ", len(rcvData))
	

main()
