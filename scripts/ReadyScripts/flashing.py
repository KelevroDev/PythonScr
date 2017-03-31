import os, time
from shutil import copyfile
import fnmatch, re
import shutil
import logging
import threading
import yaml
import paramiko
import subprocess
from Scp import SCPClient
from os.path import isfile
from os import listdir
from os.path import join as joinpath
import serial
import sys
import win32com.client as win32
import hashlib
import datetime



class SerialConnection:# Serial connection (COM)
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

def checkPartition():# Check which partition started
	print "Check Partition"
	x.run("mount")
	time.sleep(0.5)
	data = x.readOutput()
	line = ""
	for i in data:
		if i != ")":
			line = line + i
		else:
			break
	print ("LINE")
	print (line)
	if line.startswith("/dev/mmcblk0p6"):
		part = 6
		return part
		print ('PARTITION -> 6 <-')
	if line.startswith("/dev/mmcblk0p8"):
		part = 8
		return part
		print ('PARTITION -> 8 <-')
	else:
		print ("Can't find patition")
	print ("__Current__PARTITION__is__ " + str(part) + " ___")
	
def switch_partition(part):
	p = part
	res = 0
	if p == 8:
			x.run("echo -e \\\\x01\\\\x00\\\\x01\\\\x01 > /dev/mmcblk0p2")#Start from 6 partition
			x.run("sync")
			res = 6
		if p == 6:
			x.run("echo -e \\\\x00\\\\x00\\\\x00\\\\x01 > /dev/mmcblk0p2")# Start from 8 partition
			x.run("sync")
			res = 8
	print ("\nPartition swiched to " + str(res))
	return res

def reboot():
	x.run("reboot -f")
	time.sleep(20)
	x.run("root")
	time.sleep(2)
	x.run("root")
	time.sleep(2)
	x.run("version")
	time.sleep(1)
	res = readOutput()
	if res.startswith("<Filename>"):
		return 1
	else:
		reboot()

def revertPart(part):
	pa = part
	if pa == 6:
		return 8
	if pa == 8:
		return 6
	else:
		print ("ERROR_ partition error")


def flashing(partition_number):# Flashing MEU to new image
	#p = partition_number
	print "-> Start Flashing"
	print ("-> File name - " + fileName)
	time.sleep(1)
	x.run("mount /dev/sda1 /mnt")
	time.sleep(2)
	print (p) 
	p = revertPart(partition_number)
	print ("-> flashing to " + str(p) + " partition <-")
	print ("-> File name - " + fileName)
	x.run("dd if=/mnt/" + fileName + " of=/dev/mmcblk0p" + str(p))# Running flash command
	switch_partition(p)
	#if p == 8:
	#	print ("-> flashing 6 part <-")
	#	print ("-> File name - " + fileName)
	# 	x.run("dd if=/mnt/" + fileName + " of=/dev/mmcblk0p6")# Running flash command
	# 	switch_partition(p)
	# 	x.run("sync")
	# if p == 6:# can delete @IF@ and make a var for invert partition
	# 	print ("-> flashing 8 part <-")
	# 	print ("-> File name - " + fileName)
	# 	x.run("dd if=/mnt/" + fileName + " of=/dev/mmcblk0p8")# Running flash command
	# 	switch_partition(p)
	#	x.run("sync")
	time.sleep(900)
	print ("-> Flashing finished")


def flashingPrint():
	part = checkPartition()
	actualSize = os.path.getsize(imageFile)
	swSize = getSize()
	print ("Path - " + fileName)
	print ("SW - " + imageFile)
	print ("Partition - " + part)
	print ("Downloaded - " + str(swSize/actualSize) + " %")

def download_to_USB(srcPath, destMy): # Copy new image to target // not ready
	src = srcPath
	dest = destMy
	print "srcPath " + imageFile
	print "destMy " + dest
	x.run("/usr/bin/map-eth0.sh static")
	count = 0
	while count < 5:
		print "COUNT " + count
		time.sleep(1)
		count + 1
	paramikoClient.close()

def main():
	x = SerialConnection("COM9", "115200")# Paste the appropriate <COM*> 
	x.open()
	x.run("mount /dev/sda1 /mnt")
	parirtition = checkPartition()
	flashing(parirtition)
	up = reboot()
	if up == 1:
		print ("MEU flashed\nSW Version: " + imageFile + "\nPartition: " + parirtition + "\nYou can turOn the DCU")
	else:
		print("ERROR")
	x.close()


if __name__ == "__main__":
	main()



