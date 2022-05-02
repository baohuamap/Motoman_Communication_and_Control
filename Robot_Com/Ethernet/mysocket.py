import socket
import time

host = "192.168.0.1"
port = 2000


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.connect ((host, port))
	s.sendall (b'\xAB\x00\x26\x0C')        		   # Send int: 171 to D501 and 3110 to D502
	response = s.recv(65536)              		   # received text


print("---")
print("data sent: 171 (D501) 3110 (D502) " )
print ("data receive: ", response)
print ("data receive (int): ", int.from_bytes(response, byteorder="big", signed=False))

time.sleep(1)