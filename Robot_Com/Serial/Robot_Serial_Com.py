import serial
import time
from math import log
import numpy as np
import codecs


class RobotTask():
	def __init__(self):
		self.con = serial.Serial(
		port = 'COM3',\
		baudrate=19200,\
		parity=serial.PARITY_NONE,\
		stopbits=serial.STOPBITS_ONE,\
		bytesize=serial.EIGHTBITS,\
		timeout=0)
		#CurrentPos = self.RposC()
		
	def __bbc(self,input):
		sum = 0
		while input != 0:
			char = input % 0x100             # % chia lay du              #0x100 = 256 convert hex to dec tai sao la 2560
			sum = sum + char
			input = input // 0x100
			result = (sum - 0x01) // 0x100 + (sum - 0x01) % 0x100 * 0x100
		return result

	def __SplitData(self, received):
		string = []
		pos = np.zeros(6)                      # Return a new array of given shape and type, filled with zeros // array([ 0.,  0.,  0.,  0.,  0., 0.])
		while received != 0:
			char = received % 0x100
			received = received // 0x100
			string.insert(0, char - 48)        # convert ascii to number
		end = string.index(-46) + 1
		for k in range(6):
			string = string[end:-1]
			end = string.index(-4) + 1
			element = string[0: end - 1] 
			if -3 not in element:
				sign = 1
			else:
				sign = -1
				element.remove(-3)
			dot = element.index(-2)
			element.remove(-2)
			number = 0
			for i in range(len(element)):
				number = number + sign * element[i] * 10 ** (dot - i - 1)
			pos[k] = number
		return pos

	def __ReadUntil(self, bytes):
		line = bytearray()
		c = b'\x00'
		while c.find(bytes) == -1:
			c = self.con.readline()
			if c:
				line = line + c
		time.sleep(0.02)
		return line
	  
	def RposC(self):
		self.con.write(b'\x05')
		received = 0
		while received != 4:
			while self.con.inWaiting():
				received = int.from_bytes(self.con.readline(), byteorder='big', signed=False)
				if received == 4144:
					self.con.write(b'\x0101,000\x02RPOSC 1, 0\x0D\x03\x83\x03'), # recieved ACK0 -> send RPOSC command
				elif received == 4145:
					self.con.write(b'\x04')
				elif received == 5:   # received EQN
					self.con.write(b'\x100')    #send ACK0
					data = int.from_bytes(self.__ReadUntil(b'\x03'), byteorder='big', signed=False)
					result = self.__SplitData(data)
					self.con.write(b'\x101')    #send ACK1
		time.sleep(0.02)
		return np.round(result,3)

	def __CombineData(self,position):
		input = str(position[0]) + ', ' + str(position[1]) + ', ' + str(position[2]) + ', ' + str(position[3]) + ', ' + str(position[4]) + ', ' + str(position[5])
		out = 0x0130312C303030024d4f564c20302c2032302c20312c20
		for i in range(len(input)):
			out = out * 0x100 + ord(input[i])
		for _ in range(8):
			out = out * 0x1000000 + 0x2C2030
		out = out * 0x100 + 0x0D03
		return out

	def __bytes_needed(self,number): 
		return int(log(number, 256)) + 1

	def hold(self, data):
		self.con.write(b'\x05')
		received = 0
		while received != 4:
			while self.con.inWaiting():
				received = int.from_bytes(self.con.readline(), byteorder='big', signed=False)
				if received == 4144 and data == 1:
					self.con.write(b'\x01\x30\x31\x2C\x30\x30\x30\x02\x48\x4f\x4c\x44\x20\x31\x0D\x03\xA7\x02')
				if received == 4144 and data == 0:
					self.con.write(b'\x01\x30\x31\x2C\x30\x30\x30\x02\x48\x4f\x4c\x44\x20\x30\x0D\x03\xA6\x02')
				elif received == 4145:
					self.con.write(b'\x04')
				elif received == 5:   # received EQN
					self.con.write(b'\x100')    #send ACK0
					_ = int.from_bytes(self.__ReadUntil(b'\x03'), byteorder='big', signed=False)
					self.con.write(b'\x101')    #send ACK1
					
	def movL(self,position):
		global ImgArr, NowPos,CurrImg, CurrentPos
		self.con.write(b'\x05')
		received = 0
		distance = 20
		while distance > 8:
			while self.con.inWaiting():
				received = int.from_bytes(self.con.readline(), byteorder='big', signed=False)
				print(received)
				if received == 4144:
					command = self.__CombineData(position)
					command = command * 0x10000 + self.__bbc(command)
					self.con.write(command.to_bytes(self.__bytes_needed(command), 'big'))
				elif received == 4145:
					self.con.write(b'\x04')
				elif received == 5:                                                              # received EQN
					time.sleep(0.02)
					self.con.write(b'\x100')                                                     #send ACK0
					_ = int.from_bytes(self.__ReadUntil(b'\x03'), byteorder='big', signed=False)
					time.sleep(0.02)
					self.con.write(b'\x101')                                                     #send ACK1
				elif received == 4:
					while distance > 7:
						time.sleep(0.02)
						CurrentPos = self.RposC()
						distance = np.linalg.norm(position[0:3] - CurrentPos[0:3])

# def commPLC():
#     if serArd1.isOpen():
#         while (rFlag != 1):
#             while serArd1.in_waiting:
#                     recData = serArd1.readline(serArd1.in_waiting).decode('utf_8')
#                     print(recData)
#                     #print(type(recData))
#                     #print(len(recData))
#                   if str(recData[0]) == 'D':
#                      rFlag = 1

def main():
	robot = RobotTask()
	serArd1 = serial.Serial(port = 'COM3',
							baudrate = 9600,
							parity = serial.PARITY_NONE,
							stopbits = serial.STOPBITS_ONE,
							bytesize = serial.EIGHTBITS,
							timeout = 30
						)
	rFlag = 0

	if serArd1.isOpen():
		time.sleep(1)
		while (rFlag != 1):
			while serArd1.in_waiting:
				recData = serArd1.readline(serArd1.in_waiting).decode('utf_8')
				# if recData >= 1:
				#   D1 = D1 + 1
				serArd1.write("Stop".encode())
				#print(str(recData))
				if (str(recData == 'D')):
					rFlag = 1
			time.sleep(1)

	#commPLC()

	# nx100 = RobotTask()

	#recData = commPLC()
	# if recData[0] == 'D':
	#     nx100 = RobotTask()
	#     Pos = nx100.RposC()
	#     print(Pos)
		
	# time.sleep(2)
	# if D1 == "D":
	# while True:
	#     nx100 = RobotTask()
	# # Pos = nx100.RposC()
	# # # Poslater = Pos
	# # print(Pos)
	# # # Pos[1] = Pos[1] + 15
	# # nx100.movL([693.67 ,   -4.051 , 453.57 ,   78.98 ,   -5.42 ,  100.02 ])



	# # nx100 = RobotTask()
	#     Pos = nx100.RposC()
	# # Poslater = Pos
	#     print(Pos)
	#     time.sleep(5)
	# # commPLC()


	# # Pos[1] = Pos[1] + 15
	# nx100.movL([693.67 ,   -4.051 , 453.57 ,   78.98 ,   -5.42 ,  100.02 ])

	# if (rFlag == 1):
	# 	print("OK")
	# 	time.sleep(1)
	# 	Pos = robot.RposC()
	# 	print(Pos)
	# 	robot.movL([ -41.95 ,  -513.593 , -185.765 ,  178.55 ,     1.73 ,    40.02 ]) 
	# 	time.sleep(2)
	# 	robot.movL([388.889 , -59.517 ,  14.182 , 171.34 ,    8.64 ,  125.44 ])
	# 	time.sleep(2)
	# 	robot.movL([ 569.449 ,  -39.327 , -273.93 ,   177.87 ,     2.39 ,   131.38 ])
	# 	serArd1.write("Xong".encode())
		# for i in range(5):
		#     Pos[1] = Pos[1] - 30
		#     robot.movL(Pos)
		#     print(i)
		#     time.sleep(2)
		# time.sleep(2)
		# robot.movL(Pos)

main()