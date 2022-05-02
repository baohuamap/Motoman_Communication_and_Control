import serial
import time
from math import log
import numpy as np
import codecs

class RobotTask():
    def __init__(self):
        self.config = serial.Serial(
        port = 'COM5',
        baudrate=19200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=0)
	
	def __bbc(self,input):
		pass

	def __SplitData(self, received):
		pass

	def __ReadUntil(self, bytes):
		pass

	def RposC(self):
		pass

	def __CombineData(self,position):
		pass

	def __bytes_needed(self,number):
		pass

	def hold(self, data):
		pass

	def movL(self,position):
		pass