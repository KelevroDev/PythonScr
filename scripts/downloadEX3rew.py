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
#
configPath = "E:\\scripts\\UploadConfig.yaml"
f = open(configPath, 'r')
dic = yaml.load(f)
f.close()
#
#logging.basicConfig(level = logging.DEBUG)
#
pathToWeekly = dic['pathWeekly']
pathToDaily = dic['pathDaily']
pathToEng = dic['pathEng']

#
WeeklySeconds = 0
DailySeconds = 0
FilePassDaily = ""
FilePassWeekly = ""
destMy = dic['pathDst']
#destMy = "/tmp/"
#

host = dic['ip']#change target IP to your target IP
user = dic['login']
secret = dic['pass']
port = dic['portIP']



def mountSharedDir(netPath, user, password, winDrive):
    print("Connecting to [%s]" % netPath)
    os.system('NET USE %s: %s /USER:"%s" "%s"' % (winDrive, netPath, user, password))

def unmountSharedDir(winDrive):
    print("Unmounting disk [%s]" % winDrive)
    os.system('NET USE %s: /delete' % (winDrive))

#mountSharedDir("\\\\hirowsfsvs01.ad.harman.com\TOYOTA\Toyota_CY17_MEU",
#               "ADHARMAN\SKalinina",
#               "Harman/0588",
#               "Z")

ser = serial.Serial('COM9', 115200, dsrdtr = 1,timeout = 0)
global TestResults
TestResults = ' '
global stringVer
stringVer = ' '
global status
status = " "
global fileName
fileName = ''
global maxTime
global SHAremote
SHA1 = ''
global SHAhost
SHAhost = ''
maxTime = 0
imageFile = ''
def getFile(FolderPass):
	status = "Search file"
	global maxTime
	global imageFile
	global fileName
	mypath = FolderPass
	print (mypath)
	time.sleep(2)
	for line in listdir(mypath):
		if isfile(joinpath(mypath,line)):
			if line.endswith('.ext3'):
				thisFileTime = os.path.getctime(mypath + line)
				if thisFileTime > maxTime:
					maxTime = thisFileTime
					imageFile = mypath + line
					fileName = line
		else:
			for line2 in listdir(mypath + line):
				if line2.endswith('.ext3'):
					thisFileTime = os.path.getctime(mypath + line + "\\" + line2)
					if thisFileTime > maxTime:
						maxTime = thisFileTime
						imageFile = mypath + line + "\\" + line2
						fileName = line2

	print ("#######################################")
	print ("\n\n")
	print ("Time: ")
	print (maxTime)
	print ("Full path: ")
	print (imageFile)
	print ("fileName: ")
	print (fileName)
	print ("\n\n")
	print ("#######################################")

# NOT
def copyFileToTarget(srcPath, destMy):
	status = "file copying"
	src = srcPath
	dest = destMy
	paramikoClient = paramiko.SSHClient()
	paramikoClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	paramikoClient.connect(host, port, user, secret)

	scpClient = SCPClient(paramikoClient.get_transport())
	scpClient.put(imageFile, dest)

	#scpClient.close()
	#paramikoClient.close()

def progressBar():
	print("START PROGRESSBAR")
	time.sleep(1)
	getSize()
	actualSize = os.path.getsize(imageFile)
	print (actualSize)
	#while actualSize != (swSize*1000):
	while (swSize*1000)/(actualSize/100) < 97:
		getSize()
		print (swSize*1000)
		print (actualSize)
		print ("Downloaded: " + str((swSize*1000)/(actualSize/100)) + "%")
		#print ("Actual one % : " + str(actualSize/100))
		#print ("My    % : " + str(swSize))
		time.sleep(5)
		os.system('cls')
	percent = str((swSize*1000)/(actualSize/100))
	print ("DONE")
	print ("Flie " + imageFile + " on target!!!")
	print ("Starting flashing")
	return percent


def copyToUSB():
	paramikoClient = paramiko.SSHClient()
	paramikoClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	paramikoClient.connect(host, port, user, secret)

	scpClient = SCPClient(paramikoClient.get_transport())
	scpClient.put(srcPath, "/tmp/")
	scpClient.close()
	paramikoClient.close()

def checkVersion():
	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect(hostname=host, username=user, password=secret, port=int(port))
	#take a vesion
	stdin, stdout, stderr = client.exec_command("cat /etc/Toyota_CY17.XML | grep '<Filename>A'")
	data = stdout.read() + stderr.read()
	stringVer = str(data)
	return stringVer


def getSize():
	paramikoClient = paramiko.SSHClient()
	paramikoClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	paramikoClient.connect(host, port, user, secret)

	stdin, stdout, stderr = paramikoClient.exec_command("ls -s /mnt/*" + fileName + "*")
	data = stdout.read() + stderr.read()
	print ("DATA")
	print (data)
	global swSize
	swSize = 0
	sw = ""
	stringToInt = ''
	for char in data:
		if char == '/':
			break
		else:
			sw = sw + char
	for i in sw:
		if i != ' ':
			stringToInt = stringToInt + i
	swSize = int(stringToInt)
	paramikoClient.close()

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
		if self.readOutput.endswith('error'):
			print ("CAN'T FLASHING!!!")

def checkPartition():
	#x = SerialConnection("COM9", "115200")
	#x.open()
	x.run("mount")
	outPut = x.readOutput()
	print (outPut)
	if outPut.endswith('/dev/mmcblk0p6 on / type ext3'):
		part = 6
	if outPut.endswith('/dev/mmcblk0p8 on / type ext3'):
		part = 8
	return part

def flashing():
	x = SerialConnection("COM9", "115200")
	x.open()
	x.run("root")
	time.sleep(1)
	x.run("root")
	time.sleep(1)
	x.run("mount /dev/sda1 /mnt")
	time.sleep(2)
	version = checkVersion()
	#if version != fileName:
	if fileName.endswith(version) == -1:
		part = checkPartition()
		if part == 8:
			x.run("dd if=/mnt/"+ fileName + " of=/dev/mmcblk0p6")
			x.run("echo -e \\x01\\x00\\x01\\x01 > /dev/mmcblk0p2")
			x.run("sync")
		if part == 6:
			x.run("dd if=/mnt/"+ fileName + " of=/dev/mmcblk0p8")
			x.run("echo -e \\x00\\x00\\x00\\x01 > /dev/mmcblk0p2")
			x.run("sync")
	else:
		print ("ERROR - pertitions issue!!!")

	x.run("reboot -f")
	time.sleep(30)
	x.readOutput()
	x.run("root")
	time.sleep(1)
	x.run("root")
	x.readOutput()
	time.sleep(1)
	x.run("udhcpc -i eth0")
	time.sleep(10)
	ver = checkVersion()
	print (ver)
	x.close()

def checkDCU():
	paramikoClient = paramiko.SSHClient()
	paramikoClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	paramikoClient.connect(host, port, user, secret)

	stdin, stdout, stderr = paramikoClient.exec_command("ls -l /DCU/")
	data = stdout.read() + stderr.read()
	print ("DATA")
	print (data)
	if data.endswith('error'):
		print ("DCU connection FAILED!!!")
		dcu = 'ok'
	else:
		print ("DCU - connected")
		dcu = 'no'
	return dcu

################################################################################
def MainShow():
	percent = progressBar()
	while percent < 97:
		print ("""
			# # # # # # # # # # # # # # # # # # # # # # # # # #
			# FILE: """ + imageFile + """ 
			# FOLDER: """ + srcPath + """
			# 
			# ACTUAL VERSION: """ + stringVer + """
			# 
			# STATUS: """ + status + """
			# 
			# DOWNLOADING -> """ + percent + """ %
			# 
			""")

def SendEmail():
	logName = str(datetime.datetime.now())
	stringVer = "A16333BB"
	emailText = "\nSoftWare Version: " + stringVer + "\nDate: " + logName
	MailHeader = "\nHello,\nCY17 - SW " + stringVer + " was flashed and tested." + emailText
	signature = "\n\n\nCreated by:\nE. Kiriyanov\nEKiriyanov@luxoft.com"
	TestResults = "\n\nSome results - OK\nSome results - OK\nSome results - NOK\nSome results - OK\n...\n..."

	outlook = win32.Dispatch('outlook.application')
	mail = outlook.CreateItem(0)
	mail.To = 'ekiriyanov@luxoft.com'
	#mail.To = 'skalinina@luxoft.com'
	mail.Subject = "Automated test report - CY17 sw" + stringVer
	mail.body = MailHeader + TestResults + signature
	mail.send

def hash_file(filename):
	# make a hash object
	h = hashlib.sha1()
	# open file for reading in binary mode
	with open(filename,'rb') as file:

    # loop till the end of the file
		chunk = 0
		while chunk != b'':
			# read only 1024 bytes at a time
			chunk = file.read(1024)
			h.update(chunk)
    # return the hex representation of digest
	return h.hexdigest()

getFile(pathToDaily)
#print("Files checked " + str(counter))
getFile(pathToWeekly)
#print("Files checked " + str(counter))
getFile(pathToEng)
#print("Files checked " + str(counter))
#ChooseLatestFile()

#getSize()
t = threading.Thread(target=copyFileToTarget, args=(imageFile, destMy))
t.daemon = True
t.start()
SHAremote = hash_file(imageFile)
SHAhost = hash_file(destMy + "/" + fileName)
counter = 5
while counter > 0:
	print ("Wait!!! Flashing started up after: ")
	print (counter)
	time.sleep(1)
	counter = counter - 1

flashing()

