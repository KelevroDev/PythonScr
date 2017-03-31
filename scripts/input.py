
import os
import serial
import time

ser = serial.Serial('COM9', 9600, timeout=0)
 
while 1:
	try:
		ser.writeline("root")
		time.sleep(1)
		ser.writeline("root")
		time.sleep(2)
		ser.writeline("mmc dev 2")
		time.sleep(5)
		ser.writeline("mmc read 0x10800000 800 4c7e")

		ser.writeline("bootm")

		ser.writeline("mount /dev/sda1 /mnt")

		ser.writeline("flash....***")
		except ser.SerialTimeoutException:
		print('Data could not be read')
		time.sleep(1)

ser.close()



