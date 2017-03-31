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

#######################################################################################
#                                                                                     #
# Download "UploadConfig.yaml" to your PC, put the file beside this script			  #
#                                                                                     #
# Configure "UploadConfig.yaml": add your IP, COM-port, loggin, password and other	  #
#                                                                                     #
# USB should be insert to MEU all the time											  #
#                                                                                     #
# Driver(FirmwareHubEmulator) should be installed on connected PC 					  #
#                                                                                     #
#######################################################################################

# Read config file and write data to dictionary 
#configPath = "D:\\Automation\\flashing\\scripts\\UploadConfig.yaml"# Insert <your> actual path which contain "UploadConfig.yaml"
configPath = "\\UploadConfig.yaml"
f = open(configPath, 'r')
dic = yaml.load(f)
f.close()

# Global variables
global part
part = 0
global pathList
pathList = []
pathToWeekly = dic['pathWeekly']
pathToDaily = dic['pathDaily']
pathToEng = dic['pathEng']
pathList = [pathToWeekly, pathToDaily, pathToEng]
WeeklySeconds = 0
DailySeconds = 0
FilePassDaily = ""
FilePassWeekly = ""
destMy = dic['pathDst']
global host
host = dic['ip']
global user
user = dic['login']
global secret
secret = dic['pass']
global port
port = dic['portIP']
global TestResults
TestResults = ''
global stringVer
stringVer = ''
global status
status = ""
global maxTime
global SHAremote
SHA1 = ''
global SHAhost
SHAhost = ''
global version
version = 'Version '
global TestResultsBIN
TestResultsBIN = 'Binaries \n'
global TestResultsPROC
TestResultsPROC = 'Process \n'
global TestResultsSYS
TestResultsSYS = 'Services \n'
global conn
conn = "\n NO CONNECTION \n"
global percent
percent = 0# By defoult

def getFile(FolderPass, file):# Get the path of latest image
	global fileName
	global imageFile
	global maxTime
	file = file
	maxTime = 0
	status = "Searching file"
	mypath = FolderPass
	print ("Check files in - %s" % (mypath))
	time.sleep(2)
	for line in listdir(mypath):# Search files in folder 
		if isfile(joinpath(mypath,line)):
			if line.endswith(file):
				thisFileTime = os.path.getctime(mypath + line)
				if thisFileTime > maxTime:
					maxTime = thisFileTime
					imageFile = mypath + line
					fileName = line
		else:
			for line2 in listdir(mypath + line): #search files in next folder
				if line2.endswith(file):
					thisFileTime = os.path.getctime(mypath + line + "\\" + line2)
					if thisFileTime > maxTime:
						maxTime = thisFileTime
						imageFile = mypath + line + "\\" + line2
						fileName = line2 # Save file name
	print ("\n\n")
	print ("Full path: ")
	print (imageFile)
	print ("fileName: ")
	print (fileName)
	print ("\n\n")
	print ("Destination path - \n" + destMy)

def copyFileToTarget(srcPath, destMy): # Copy new image to target
	status = "file copying"
	src = srcPath
	dest = destMy
	paramikoClient = paramiko.SSHClient()
	paramikoClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	paramikoClient.connect(host, port, user, secret)
	scpClient = SCPClient(paramikoClient.get_transport())
	print "srcPath " + imageFile
	print "destMy " + dest
	scpClient.put(imageFile, dest)
	count = 0
	while count < 5:
		print "COUNT " + count
		time.sleep(1)
		count + 1
	paramikoClient.close()

def progressBar(t):# Show actual progress bar(%)
	print ("FileName - " + imageFile)
	print("START PROGRESSBAR")
	time.sleep(5)
	actualSize = os.path.getsize(imageFile)# Source file size
	while t.isAlive():
		print ("Downloading...")
		swSize = getSize()
		print (swSize*1000)
		print (actualSize)
		print ("Downloaded: " + str((swSize*1000)/(actualSize/100)) + "%")# Shows the result as a percentage of download
		time.sleep(5)
		os.system('cls')
	print ("Actual size - ", actualSize)
	count = 10
	while count > 0:# Time for cleaning buffer
		time.sleep(1)
		count = count - 1
		print "Wait - " + str(count)
	print ("DONE")
	print ("Flie " + imageFile + " on target!!!")
	print ("Starting flashing")

def copyToUSB(srcPath):# Copy new image to USB
	paramikoClient = paramiko.SSHClient()
	paramikoClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	paramikoClient.connect(host, port, user, secret)
	scpClient = SCPClient(paramikoClient.get_transport())
	scpClient.put(srcPath, "/tmp/")
	scpClient.close()
	paramikoClient.close()

def checkVersion():# Check current version
	print ("Check Version")
	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect(hostname=host, username=user, password=secret, port=int(port))
	stdin, stdout, stderr = client.exec_command("cat /etc/Toyota_CY17.XML | grep '<Filename>A'")
	data = stdout.read() + stderr.read()
	stringVer = str(data)
	print ("Version is %s *** *** ***" % stringVer)
	return stringVer

def getSize():# Get new/current image version 
	print ("FileName - ", fileName)
	print ("Getting SIZE")
	paramikoClient = paramiko.SSHClient()
	paramikoClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	paramikoClient.connect(host, port, user, secret)
	stdin, stdout, stderr = paramikoClient.exec_command("ls -s /mnt*" + fileName + "*")
	data = stdout.read() + stderr.read()
	swSize = 0# Size by default 
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
	print "SW SIZE", stringToInt
	swSize = int(stringToInt)
	print "SW SIZE", swSize
	paramikoClient.close()
	return swSize

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
	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect(hostname=host, username=user, password=secret, port=int(port))# Connect to MEU via IP address
	stdin, stdout, stderr = client.exec_command("mount")
	data = stdout.read() + stderr.read()
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
	print ("__Current__PARTITION__is__" + str(part) + "___")
	client.close()

def flashing():# Flashing MEU to new image
	print "Start Flashing"
	x = SerialConnection("COM9", "115200")# Paste the appropriate <COM*> 
	x.open()
	print ("File name - " + fileName)
	x.run("root")
	time.sleep(1)
	x.run("root")
	time.sleep(2)
	x.run("udhcpc -i eth0")
	time.sleep(1)
	x.run("mount /dev/sda1 /mnt")
	time.sleep(2)
	p = checkPartition()
	print (p) 
	if p == 8:
		print ("-> flashing 6 part <-")
		print ("File name - " + fileName)
		x.run("dd if=/mnt/" + fileName + " of=/dev/mmcblk0p6")# Running flash command
		time.sleep(900)
		x.run("umount /mnt")
		x.run("echo -e \\\\x01\\\\x00\\\\x01\\\\x01 > /dev/mmcblk0p2")#Start from 6 partition
		x.run("sync")
	if p == 6:
		print ("-> flashing 8 part <-")
		print ("File name - " + fileName)
		x.run("dd if=/mnt/" + fileName + " of=/dev/mmcblk0p8")# Running flash command
		time.sleep(900)
		x.run("umount /mnt")
		x.run("echo -e \\\\x00\\\\x00\\\\x00\\\\x01 > /dev/mmcblk0p2")# Start from 8 partition
		x.run("sync")
	else:
		print ("ERROR - partitions issue!!!")
	print ("FLASHED")
	time.sleep(1)
	print ("STARTING REBOOT")
	x.run("reboot -f")# Hard reboot
	counter = 30
	while counter > 0: 
		time.sleep(1)
		print "Wait till rebooting " + str(counter)
		counter = counter - 1
	x.run("root")# loggin
	time.sleep(1)
	x.run("root")# password
	time.sleep(1)
	print ("ETHERNET CONNECTION")
	x.run("udhcpc -i eth0")
	time.sleep(5)
	checkPartition()
	time.sleep(2)
	x.run("version")
	x.close()

def checkVersion():#Test; Check Version
	global version
	version = 'Version '
	print ("Check Version")
	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect(hostname=host, username=user, password=secret, port=int(port))
	stdin, stdout, stderr = client.exec_command("cat /etc/Toyota_CY17.XML | grep '<Filename>A'")
	data = stdout.read() + stderr.read()
	stringVer = str(data)
	print (stringVer)
	version = stringVer[12:19]
	return version

def checkDCU():# Check DCU connection
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
	client.close()

def bin_check():#Test; Check binaries
	global TestResultsBIN
	TestResultsBIN = 'Binaries \n'
	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect(hostname=host, username=user, password=secret, port=int(port))
	stdin, stdout, stderr = client.exec_command("find /usr/bin/ *")
	data = stdout.read() + stderr.read()
	f2 = open('D:\Automation\\flashing\scripts\Testing\list-of-bin.textile', 'r')
	bin_str_good = "\n binaries OK--------- \n\n"
	bin_str_bad = "\n binaries NOK--------- \n\n"
	print ("-> BINARIES <-")
	for val in f2:
		if data.find(val.strip()) == -1:
			bin_str_bad = (bin_str_bad + val.strip() +'\n')
			print (val.strip() + "	- NOK")
		else:
			bin_str_good = (bin_str_good + val.strip() +'\n')
			print (val.strip() + "	- OK")
	TestResultsBIN = "\n\n" + bin_str_good + bin_str_bad + "\n\n"
	print TestResultsBIN
	return TestResultsBIN
	client.close()


def proc_check():#Test; Check list of processes
	global TestResultsPROC
	TestResultsPROC = 'Process '
	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect(hostname=host, username=user, password=secret, port=int(port))
	stdin, stdout, stderr = client.exec_command("ps /lib/systemd/system")
	data = stdout.read() + stderr.read()
	logName = str(datetime.datetime.now())
	f2 = open('D:\Automation\\flashing\scripts\Testing\list-of-process.textile','r')
	proc_str_good = "\n processes OK <- \n\n"
	proc_str_bad = "\n processes NOK <- \n\n"
	stdin, stdout, stderr = client.exec_command("ps")
	data = stdout.read() + stderr.read()
	print ("-> PROCESSES <-")
	for val in f2:
		if data.find(val.strip()) == -1:
			proc_str_bad = (proc_str_bad + val.strip() +'\n')
			print (val.strip() + "	-> NOK")
		else:
			proc_str_good = (proc_str_good + val.strip() +'\n')
			print (val.strip() + " -> OK")
	TestResultsPROC = (proc_str_good + proc_str_bad + "\n\n")
	return TestResultsPROC
	client.close()

def SendEmail():#Send eMail with/without test results
	print ("Sending e-mail")
	nowTime = str(datetime.datetime.now())
	emailText = "\nDate: " + nowTime
	MailHeader = "Hello,\nCY17 - SW " + version + " was flashed and tested." + emailText
	signature = "\n\n\nCreated by:\nE. Kiriyanov\nEKiriyanov@luxoft.com"
	outlook = win32.Dispatch('outlook.application')
	mail = outlook.CreateItem(0)
	mail.To = 'ekiriyanov@luxoft.com'#insert email recipients
	mail.Subject = "Automated test report - CY17 sw " + version
	mail.body = MailHeader + conn + TestResultsBIN + TestResultsPROC + TestResultsSYS + signature
	mail.send
	print ("E-mail sended")
	client.close()

def sys_check():#Test; Check service
	global TestResultsSYS
	TestResultsSYS = 'Services '
	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect(hostname=host, username=user, password=secret, port=int(port))
	stdin, stdout, stderr = client.exec_command("ls -l /lib/systemd/system")
	data = stdout.read() + stderr.read()
	logName = str(datetime.datetime.now())
	f2 = open('D:\Automation\flashing\scripts\Testing\list-of-serv.textile', 'r')
	serv_str_good = "\n services OK <- \n\n"
	serv_str_bad = "\n services NOK <- \n\n"
	print ("-> SERVICES <-\033[1;m")
	for val in f2:
		if data.find(val.strip()) == -1:
			serv_str_bad = (serv_str_bad + val.strip() +'\n')
			print (val.strip() + "	-> NOK")
		else:
			serv_str_good = (serv_str_good + val.strip() +'\n')
			print (val.strip() + "	-> OK")
	TestResultsSYS = (serv_str_good + serv_str_bad + "\n\n")
	return TestResultsSYS
	client.close()

def Connection():#Check internet connection on the target
	ping = os.popen('ping :192.168.137.2')
	result = ping.readlines()
	msLine = result[3].strip()
	print (result)
	print ("MSLINE - " + msLine)
	print msLine[40:41]
	if msLine == "Reply from 192.168.137.2: Destination host unreachable.":
		print "-> NOK"
	else:
		print "-> OK"
	return msLine

def hash_file(filename):#Get SHA1 summ
	print ("calculate the sum SHA1")
	h = hashlib.sha1()
	with open(filename,'rb') as file:
		chunk = 0
		while chunk != b'':
			chunk = file.read(1024)
			h.update(chunk)
	return h.hexdigest()

def mountUSB():# Mount USB to MEU.
	print ("MOUNT USB")
	x = SerialConnection("COM9", "115200")
	x.open()
	time.sleep(2)
	x.run("root")
	time.sleep(2)
	x.run("root")
	time.sleep(2)
	x.run("mount /dev/sda1 /mnt/")
	time.sleep(2)
	x.run("udhcpc -i eth0")
	
	time.sleep(2)
	x.close()

def runTests():# Run tests; Simple tests to check MEU alive or not.
	res = Connection()
	print "res - "
	print (res)
	if res == "Reply from 10.67.69.240: Destination host unreachable.":
		print 'Connection failed!'
		SendEmail()
	else:
		checkVersion()
		bin_res = bin_check()
		proc_res = proc_check()
		sys_check()
		SendEmail()

def main():
	mountUSB()
	print("STARTING")
	print ("Getting file")
	checkPartition()
	mountUSB()
	for i in pathList:
		getFile(i, 'rootfs.ext3')
	print "FILE FOR FLASHING - " + imageFile
	time.sleep(5)
	t = threading.Thread(target=copyFileToTarget, args=(imageFile, destMy))
	t.daemon = True
	t.start()
	progressBar(t)
	counter = 5
	while counter > 0:
		print ("Wait!!! Flashing started up after: ")
		print (str(counter) + " sec")
		time.sleep(1)
		counter = counter - 1
	flashing()
	dcu = checkDCU()
	if dcu == "ok":
		runTests()
		SendEmail()
	if dcu == "no":
		print "DCU IS NOT CONNECTED"
		print "Try to reboot MEU"
		x = SerialConnection("COM9", "115200")
		x.open()
		x.run("reboot -f")
		time.sleep(30)
		dcu = checkDCU()
		x.close()
		if dcu == "ok":
			runTests()
			SendEmail()
		else:
			print "DCU STILL NOT CONNECTED!!!"
			print "Please check DCU connection."
			SendEmail()

if __name__ == "__main__":
	main()