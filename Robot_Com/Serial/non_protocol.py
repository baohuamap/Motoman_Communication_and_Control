import serial
import time

def com_PLC(ser):
	rFlag = 0
	if ser.isOpen():
		print("port is open")
		time.sleep(1)
	while (rFlag != 1):
		while ser.in_waiting:
			rcvData = ser.readline(ser.in_waiting).decode('utf_8')     # receive data
			ser.write("Hello PLC".encode())                            # send data
			if (str(rcvData == 'HI BAO')):
				rFlag = 1
				print("--- Received Data ---")
				print("Data received: ", rcvData)
		time.sleep(1)

def main():
	ser = serial.Serial(port = 'COM3', 
					baudrate=9600,
					parity=serial.PARITY_NONE, 
					stopbits=serial.STOPBITS_ONE,
					bytesize=serial.EIGHTBITS, 
					timeout=0)

	com_PLC(ser)


main()
