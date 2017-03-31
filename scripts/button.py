# -*- coding: utf-8 -*-

import time
import serial
from os.path import isfile
from os import listdir
from os.path import join as joinpath
import paramiko
import datetime
import stat, sys, os, string, commands
import argparse
reload(sys)
sys.setdefaultencoding('utf-8')
#str = unicode(str, errors='ignore')

class SerialConnection:
	def __init__(self, port, speed):
		self.port = port
		self.speed = speed
		self.timeout = 0.5
		self.obj = None

	def open(self):
		self.obj = serial.Serial(self.port, self.speed)
		if self.obj.is_open:
			print("Device connected")
			self.readOutput()

	def close(self):
		self.obj.close()

	def run(self, command):
		if self.obj is not None:
			if self.obj.is_open:
				self.obj.write((command + "\r\n").encode())
				time.sleep(self.timeout)
				self.readOutput()
			else:
				print("ERROR: connection is not opened")
		else:
			print("ERROR: communication object does not exist")

	def readOutput(self):
		output = str()
		while self.obj.inWaiting() > 0:
			output += self.obj.read(1).decode()
		if len(output):
			print(output)

global part
part = 0

def checkPartition():
	#x = SerialConnection("COM9", "115200")
	#x.open()
	global part
	part = 0
	host = '10.67.68.67'
	user = "root"
	secret = "root"
	port = 22
	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	
	client.connect(hostname=host, username=user, password=secret, port=int(port))
	
	stdin, stdout, stderr = client.exec_command("mount")
	data = stdout.read() + stderr.read()
	line = ""
	for i in data:
		#print (i)
		if i != ")":
			line = line + i
		else:
			break
	print ("LINE")
	print (line)
	if line.startswith("/dev/mmcblk0p6"):
		part = 6
		print ('PARTITION - 6***************************')
	if line.startswith("/dev/mmcblk0p8"):
		part = 8
		print ('PARTITION - 8***************************')
	else:
		print ("EMPTY!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
	print ("___________PARTITION IS " + str(part) + "______")
	#client.close()

def flashing():
	x = SerialConnection("COM9", "115200")
	x.open()
	x.run("root")
	time.sleep(1)
	x.run("root")
	time.sleep(1)
	x.run("mount /dev/sda1 /mnt")
	time.sleep(2)
	
	if part == 8:
		print ("########################## flashing 6 part ##############")
		x.run("dd if=/mnt/TOYOTA_CY17_MEU_A16262A_AppOnlDiagHMISWSysSWUpdVR_A+.rootfs.ext3 of=/dev/mmcblk0p6")
		time.sleep(900)
		x.run("echo -e \\x01 > /dev/mmcblk0p2")
		x.run("sync")
	if part == 6:
		print ("########################## flashing 8 part ##############")
		x.run("dd if=/mnt/TOYOTA_CY17_MEU_A16262A_AppOnlDiagHMISWSysSWUpdVR_A+.rootfs.ext3 of=/dev/mmcblk0p8")
		time.sleep(900)
		x.run("echo -e \\x00 > /dev/mmcblk0p2")
		#print (switchCommand8)
		x.run("sync")
	else:
		print ("ERROR - partitions issue!!!")
	print ("FLASHED")
	time.sleep(1)

	print ("STARTING REBOOT")
	x.run("reboot -f")
	time.sleep(30)
	x.readOutput()
	x.run("root")
	time.sleep(1)
	x.run("root")
	x.readOutput()
	time.sleep(1)
	x.run("udhcpc -i eth0")
	time.sleep(5)
	#ver = checkVersion()
	x.run("version")
	time.sleep(2)
	x.run("mount")
	#print (ver)
	x.close()

def connection():
	x = SerialConnection("COM9", "115200")
	x.open()
	print ("LOGIN")
	x.run("root")
	time.sleep(2)
	print ("PASSWORD")
	x.run("root")
	time.sleep(1)
	print ("ETHERNET")
	x.run("udhcpc -i eth0")
	time.sleep(2)
	x.close()

print ("Connection")
connection()
print ("Check Partition")
checkPartition()
print ("Flashing")
flashing()