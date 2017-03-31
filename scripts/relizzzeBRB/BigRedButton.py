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
import psutil

configPath = "D:\\Automation\\flashing\\scripts\\UploadConfig.yaml"
f = open(configPath, 'r')
dic = yaml.load(f)
f.close()

global part
part = 0
global pathList
pathList = []
pathToWeekly = dic['pathWeekly']
pathToDaily = dic['pathDaily']
pathToEng = dic['pathEng']
nameR = dic['nameR']
nameU = dic['nameU']
pathList = [pathToWeekly, pathToDaily, pathToEng]
WeeklySeconds = 0
DailySeconds = 0
FilePassDaily = ""
FilePassWeekly = ""

global destMy
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
global percent
percent = 0

def uploadConfig(dic):
	f = open(configPath, "w")
	f.write(yaml.dump(dic, default_flow_style=False))
	f.close()

def getRoot(FolderPass):
	global fileName
	global imageFile
	global maxTime
	maxTime = 0
	status = "Searching file"
	mypath = FolderPass
	print ("Check files in - %s" % (mypath))
	time.sleep(2)
	for line in listdir(mypath):#search files in folder 
		if isfile(joinpath(mypath,line)):
			if line.endswith('rootfs.ext3'):
				thisFileTime = os.path.getctime(mypath + line)
				if thisFileTime > maxTime:
					maxTime = thisFileTime
					imageFile = mypath + line
					fileName = line
			#if line.startswith('uImage--'):
				
		else:
			for line2 in listdir(mypath + line):#search files in next folder
				if line2.endswith('rootfs.ext3'):
					thisFileTime = os.path.getctime(mypath + line + "\\" + line2)
					if thisFileTime > maxTime:
						maxTime = thisFileTime
						imageFile = mypath + line + "\\" + line2#save full path to file
						fileName = line2#save file name
	print ("Full path: ", imageFile)
	print ("fileName: ", fileName)
	print ("Destination path - \n" + destMy)
	return imageFile

def getUimage(FolderPass):
	global fileNameU
	global imageFileU
	global maxTime
	maxTime = 0
	status = "Searching Uimage file"
	mypath = FolderPass
	print ("Check Uimage files in - %s" % (mypath))
	time.sleep(2)
	for line in listdir(mypath):#search files in folder 
		if isfile(joinpath(mypath,line)):
			if line.startswith('uImage--'):
				thisFileTime = os.path.getctime(mypath + line)
				if thisFileTime > maxTime:
					maxTime = thisFileTime
					imageFileU = mypath + line
					fileNameU = line
			#if line.startswith('uImage--'):
				
		else:
			for line2 in listdir(mypath + line):#search files in next folder
				if line2.startswith('uImage--'):
					thisFileTime = os.path.getctime(mypath + line + "\\" + line2)
					if thisFileTime > maxTime:
						maxTime = thisFileTime
						imageFileU = mypath + line + "\\" + line2#save full path to file
						fileNameU = line2#save file name
	print ("\n\n")
	print ("Uimage Full path: ")
	print (imageFileU)
	print ("Uimage fileName: ")
	print (fileNameU)
	print ("\n\n")
	print ("Destination path - \n" + destMy)
	return imageFileU

def copyFileToTarget(srcPath, destMy):
	File = srcPath
	status = "file copying"
	src = srcPath
	dest = destMy
	paramikoClient = paramiko.SSHClient()
	paramikoClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	paramikoClient.connect(host, port, user, secret)
	scpClient = SCPClient(paramikoClient.get_transport())
	print "srcPath " + imageFile
	print "destMy " + dest
	scpClient.put(File, dest)
	count = 0
	while count < 5:
		print ("COUNT " + str(count))
		time.sleep(1)
		count = count + 1
	paramikoClient.close()

def progressBar(t, name, fullPath):
	print ("FileName - " + name)
	print("START PROGRESSBAR")
	time.sleep(5)
	actualSize = os.path.getsize(fullPath)#Source file size
	while t.isAlive():
		print ("Downloading...")
		time.sleep(10)
		swSize = getSize(name)
		print (swSize*1000)
		print (actualSize)
		print ("Downloaded: " + str((swSize*100)/(actualSize)) + "%")#Shows the result as a percentage of download
		time.sleep(5)
		os.system('cls')
	print ("Actual size - ", actualSize)
	count = 10
	while count > 0:#Time for cleaning buffer
		time.sleep(1)
		count = count - 1
		print "Wait - " + str(count)
	print ("DONE")
	print ("Flie " + name + " on target!!!")
	print ("Starting flashing")

def copyToUSB():
	paramikoClient = paramiko.SSHClient()
	paramikoClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	paramikoClient.connect(host, port, user, secret)
	scpClient = SCPClient(paramikoClient.get_transport())
	scpClient.put(srcPath, "/tmp/")
	scpClient.close()
	paramikoClient.close()

def getSize(file):
	file = file
	x = SerialConnection("COM9", "115200")
	x.open()
	x.run("/usr/bin/map-eth0.sh static")
	print ("FileName - ", file)
	print ("Getting SIZE")
	paramikoClient = paramiko.SSHClient()
	paramikoClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	paramikoClient.connect(host, port, user, secret)
	stdin, stdout, stderr = paramikoClient.exec_command("ls -s /mnt/" + file)
	data = stdout.read() + stderr.read()
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
			print (stringToInt)
	print ("SW SIZE " + str(stringToInt))
	swSize = int(stringToInt)
	print ("SW SIZE ", swSize)
	paramikoClient.close()
	return swSize
	x.close()

class SerialConnection:
	def __init__(self, port, speed):
		self.port = port
		self.speed = speed
		self.timeout = 0.5
		self.obj = None
		self.output = ''

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
		output = ''
		while self.obj.inWaiting() > 0:
			output += self.obj.read(1).decode()
		if len(output):
			print(output)

def checkPartition():
	print ("CHECK PARTITION")
	x = SerialConnection("COM9", "115200")
	x.open()
	time.sleep(3)
	x.run("/usr/bin/map-eth0.sh static")
	time.sleep(3)
	print "Check Partition"
	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect(hostname=host, username=user, password=secret, port=int(port))
	stdin, stdout, stderr = client.exec_command("mount")
	data = stdout.read() + stderr.read()
	print("DATA MOUNT ->")
	print data
	line = ""
	for i in data:
		if i != " ":
			line = line + i
		else:
			break
	print ("LINE")
	print (line)
	if line.startswith("/dev/mmcblk0p6"):
		part = 6
		return part
		print ('PARTITION - 6***************************')
	if line.startswith("/dev/mmcblk0p8"):
		part = 8
		return part
		print ('PARTITION - 8***************************')
	else:
		print ("Can't find patition")
	print ("___Current__PARTITION is " + str(part) + "______")
	client.close()
	x.close()

def flashing2():# TEST
	print "Start Flashing"
	x = SerialConnection("COM9", "115200")
	x.open()
	print ("File name - " + fileName)
	x.run("root")
	time.sleep(1)
	x.run("P!*x6kBv")
	time.sleep(2)
	time.sleep(1)
	x.run("mount /dev/sda1 /mnt")
	time.sleep(2)
	x.close()
	p = checkPartition()
	print (p) 
	x = SerialConnection("COM9", "115200")
	x.open()
	time.sleep(3)
	if p == 8:
		print ("---- flashing 6 part ----")
		print ("File name - " + fileName)
		x.run("dd if=/mnt/" + fileName + " of=/dev/mmcblk0p6")
		time.sleep(900)
		x.run("umount /mnt")
		x.run("echo -e \\\\x01\\\\x00\\\\x01\\\\x01 > /dev/mmcblk0p2")#Start from 6 partition
		x.run("sync")
	if p == 6:
		print ("---- flashing 8 part ----")
		print ("File name - " + fileName)
		x.run("dd if=/mnt/" + fileName + " of=/dev/mmcblk0p8")
		time.sleep(900)
		x.run("umount /mnt")
		x.run("echo -e \\\\x00\\\\x00\\\\x00\\\\x01 > /dev/mmcblk0p2")#Start from 8 partition
		x.run("sync")
	else:
		print ("ERROR - partitions issue!!!")
	print ("FLASHED")
	time.sleep(1)
	x = SerialConnection("COM9", "115200")
	x.open()
	print ("STARTING REBOOT")
	x.run("reboot -f")
	x.close()
	counter = 60
	while counter > 0: 
		print "Wait till rebooting " + str(counter)
		counter = counter - 1
		time.sleep(1)
	x = SerialConnection("COM9", "115200")
	x.open()
	x.run("root")
	time.sleep(1)
	x.run("P!*x6kBv")
	time.sleep(1)
	print ("ETHERNET CONNECTION")
	x.run("/usr/bin/map-eth0.sh static")
	time.sleep(5)
	#checkPartition()
	time.sleep(2)
	x.run("version")
	x.close()

def flashing(fileName, fileNameU, flash):
	print "Start Flashing"
	x = SerialConnection("COM9", "115200")
	x.open()
	print ("File name - " + fileName)
	x.run("root")
	time.sleep(1)
	x.run("P!*x6kBv")
	time.sleep(2)
	time.sleep(1)
	x.run("mount /dev/sda1 /mnt")
	time.sleep(2)
	x.close()
	p = checkPartition()
	print ("Partition is " + str(p)) 
	x = SerialConnection("COM9", "115200")
	x.open()
	time.sleep(3)
	if p == 8:
		print ("---- flashing 6 part ----")
		print ("RootFS File name - " + fileName)
		print ("uImage File name - " + fileNameU)
		x.run("dd if=/mnt/" + fileName + " of=/dev/mmcblk0p6")
		time.sleep(900)
		print ("RootFS File name - " + fileName + "DONE")
		if flashU == 0:
			x.run("dd if=/mnt/" + fileNameU + " of=/dev/mmcblk0p5")
			print ("RootFS File name - " + fileNameU + "DONE")
			time.sleep(5)
		#x.run("umount /mnt")
		x.run("echo -e \\\\x01\\\\x00\\\\x01\\\\x01 > /dev/mmcblk0p2")#Start from 6 partition
		x.run("sync")
	if p == 6:
		print ("---- flashing 8 part ----")
		print ("RootFS File name - " + fileName)
		print ("uImage File name - " + fileNameU)
		x.run("dd if=/mnt/" + fileName + " of=/dev/mmcblk0p8")
		time.sleep(900)
		if flashU == 0:
			x.run("dd if=/mnt/" + fileNameU + " of=/dev/mmcblk0p7")
			print ("RootFS File name - " + fileNameU + "DONE")
			time.sleep(5)
		#x.run("umount /mnt")
		x.run("echo -e \\\\x00\\\\x00\\\\x00\\\\x01 > /dev/mmcblk0p2")#Start from 8 partition
		x.run("sync")
	else:
		print ("ERROR - partitions issue!!!")
	print ("FLASHED")
	time.sleep(1)
	x = SerialConnection("COM9", "115200")
	x.open()
	print ("STARTING REBOOT")
	x.run("reboot -f")
	x.close()
	counter = 60
	while counter > 0: 
		print "Wait till rebooting " + str(counter)
		counter = counter - 1
		time.sleep(1)
	x = SerialConnection("COM9", "115200")
	x.open()
	x.run("root")
	time.sleep(1)
	x.run("P!*x6kBv")
	time.sleep(1)
	print ("ETHERNET CONNECTION")
	x.run("/usr/bin/map-eth0.sh static")
	time.sleep(5)
	#checkPartition()
	time.sleep(2)
	x.run("version")
	x.close()

def checkDCU():
	x = SerialConnection("COM9", "115200")
	x.open()
	time.sleep(3)
	x.run("/usr/bin/map-eth0.sh static")
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
	x.close()

def bin_check():
	x = SerialConnection("COM9", "115200")
	x.open()
	time.sleep(3)
	x.run("/usr/bin/map-eth0.sh static")
	global TestResultsBIN
	TestResultsBIN = 'Binaries \n'
	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect(hostname=host, username=user, password=secret, port=int(port))
	stdin, stdout, stderr = client.exec_command("find /usr/bin/ *")
	data = stdout.read() + stderr.read()
	f2 = open('D:\Automation\\flashing\scripts\Testing\list-of-bin.textile', 'r')
	bin_str_good = "\n Binaries are found \n\n"
	bin_str_bad = "\nList of NOT found Binaries \n\n"
	print ("---------------------------------BINARIES---------------------------------")
	for val in f2:
		if data.find(val.strip()) == -1:
			bin_str_bad = (bin_str_bad + val.strip() +'\n')
			print (val.strip() + "	- Binaries are NOT found")
		else:
			bin_str_good = (bin_str_good + val.strip() +'\n')
			print (val.strip() + "	- Binaries are found")
	#TestResultsBIN = "\n\n" + bin_str_good + bin_str_bad + "\n\n"
	TestResultsBIN = "\n\n" + bin_str_bad + "\n\n"
	return TestResultsBIN
	client.close()
	x.close()

def checkVersion():
	global version
	version = 'Version '
	x = SerialConnection("COM9", "115200")
	x.open()
	x.run("/usr/bin/map-eth0.sh static")
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
	x.close()

def proc_check():
	global TestResultsPROC
	TestResultsPROC = 'Process '
	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect(hostname=host, username=user, password=secret, port=int(port))
	stdin, stdout, stderr = client.exec_command("ps /lib/systemd/system")
	data = stdout.read() + stderr.read()
	logName = str(datetime.datetime.now())
	f2 = open('D:\Automation\\flashing\scripts\Testing\list-of-process.textile','r')
	proc_str_good = "\n Processes are running--------- \n\n"
	proc_str_bad = "\n List of NOT found Processes--------- \n\n"
	stdin, stdout, stderr = client.exec_command("ps")
	data = stdout.read() + stderr.read()
	print ("---------------------------------PROCESSES---------------------------------")
	for val in f2:
		if data.find(val.strip()) == -1:
			proc_str_bad = (proc_str_bad + val.strip() +'\n')
			print (val.strip() + "	- Processes are NOT running")
		else:
			proc_str_good = (proc_str_good + val.strip() +'\n')
			print (val.strip() + " Processes are running")
	#TestResultsPROC = (proc_str_good + proc_str_bad + "\n\n")
	TestResultsPROC = (proc_str_bad + "\n\n")
	return TestResultsPROC
	client.close()

def SendEmail():
	print ("Sending e-mail")
	nowTime = str(datetime.datetime.now())
	emailText = "\nDate: " + nowTime
	MailHeader = "Hello,\nCY17 - SW " + version + " Has been flashed and tested." + emailText
	signature = "\n\n\nCreated by:\nE. Kiriyanov\nEKiriyanov@luxoft.com"
	outlook = win32.Dispatch('outlook.application')
	mail = outlook.CreateItem(0)
	#mail.To = 'ekiriyanov@luxoft.com; skalinina@luxoft.com; dleu@luxoft.com'
	mail.To = 'ekiriyanov@luxoft.com'
	mail.Subject = "Automated test report - CY17 sw " + version
	mail.body = MailHeader + TestResultsBIN + TestResultsPROC + TestResultsSYS + signature
	mail.send
	print ("E-mail sended" + str(nowTime))

def sys_check():
	x = SerialConnection("COM9", "115200")
	x.open()
	time.sleep(3)
	x.run("/usr/bin/map-eth0.sh static")
	global TestResultsSYS
	TestResultsSYS = 'Services '
	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect(hostname=host, username=user, password=secret, port=int(port))
	stdin, stdout, stderr = client.exec_command("ls -l /lib/systemd/system")
	data = stdout.read() + stderr.read()
	logName = str(datetime.datetime.now())
	f2 = open('D:\Automation\\flashing\scripts\Testing\list-of-serv.textile', 'r')
	serv_str_good = "\n Service files are found \n\n"
	serv_str_bad = "\nList of NOT found Service files\n\n"
	print ("---------------------------------SERVICES---------------------------------\033[1;m")
	for val in f2:
		if data.find(val.strip()) == -1:
			serv_str_bad = (serv_str_bad + val.strip() +'\n')
			print (val.strip() + "	- Service files are NOT found")
		else:
			serv_str_good = (serv_str_good + val.strip() +'\n')
			print (val.strip() + "	- Service files are found")
	#TestResultsSYS = (serv_str_good + serv_str_bad + "\n\n")
	TestResultsSYS = (serv_str_bad + "\n\n")
	return TestResultsSYS
	client.close()
	x.close()

def Connection():
	x = SerialConnection("COM9", "115200")
	x.open()
	x.run("/usr/bin/map-eth0.sh static")
	#pri = x.read()
	x.colse()
	#if pri.endswith('does not exist'):
	#	print("NO USB")
	#	return 1
	
def hash_file(filename):
	print ("calculate the sum SHA1")
	h = hashlib.sha1()
	with open(filename,'rb') as file:
		chunk = 0
		while chunk != b'':
			chunk = file.read(1024)
			h.update(chunk)
	return h.hexdigest()

def mountUSB():
	print ("MOUNT USB")
	x = SerialConnection("COM9", "115200")
	x.open()
	time.sleep(2)
	x.run("root")
	time.sleep(2)
	x.run("P!*x6kBv")
	time.sleep(2)
	x.run("/usr/bin/map-eth0.sh static")
	time.sleep(5)
	x.run("cd //")
	time.sleep(1)
	########################################################
	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect(hostname=host, username=user, password=secret, port=int(port))
	stdin, stdout, stderr = client.exec_command("mount /dev/sda1 /mnt/")
	data = stdout.read() + stderr.read()
	print (data)
	#if data.find("is already mounted"):
	#	print("is already mounted")
	if "does not exist" in data:
		print("NO USB")
		client.close()
		x.close()
		return 1
	else:
		print ("is already mounted")
	client.close()
	########################################################

	time.sleep(2)
	x.close()
	return 0

def runTests():
	checkVersion()
	bin_res = bin_check()
	proc_res = proc_check()
	sys_check()
	SendEmail()

def FlashingProcess(f):
	print ("FlashingProcess")
	coun = 0
	while f.isAlive():
		coun = coun + 1
		print ("remaining time " + str(coun) + "\n FLASHING: PLEASE DON'T TURN OFF THE MEU!!!")
		print ("Will be -  ", fileName)
		time.sleep(5)
		os.system('cls')

def killer():
	PROCNAME1 = "putty.exe"
	PROCNAME2 = "ttermpro.exe"
	procFind = 0
	for proc in psutil.process_iter():
	    if proc.name() == PROCNAME1:
	        proc.kill()
	        procFind = 1
	        print ("putty - killed")
	for proc in psutil.process_iter():
	    if proc.name() == PROCNAME2:
	        proc.kill()
	        procFind = 1
	        print ("ttermpro - killed")
	if procFind == 0:
	    print ("No process COM# running")
	time.sleep(2)

def main():
	killer()
	conn = mountUSB()
	if conn == 0:
		print("STARTING")
		print ("Getting file")
		checkPartition()
		flash = 0
		###########################
		for i in pathList:
			rootFS = getRoot(i)
			uimage = getUimage(i)
		print ("rootfs - " + rootFS + "\nuimage - " + uimage)
		print ("rootfs - " + fileName + "\nuimage - " + fileNameU)
		time.sleep(5)
		print (destMy)
		if nameR != fileName:
			destMyRoot = destMy + fileName
			t = threading.Thread(target=copyFileToTarget, args=(rootFS, destMyRoot))
			t.daemon = True
			t.start()
			progressBar(t, fileName, imageFile)
			dic['nameR'] = fileName
			uploadConfig(dic)
		else:
			flash = 1
			print("This version is already installed - " + fileName)
		if nameU != fileNameU:
			destMyUimage = destMy + fileNameU
			b = threading.Thread(target=copyFileToTarget, args=(uimage, destMyUimage))
			b.daemon = True
			b.start()
			progressBar(b, fileNameU, imageFileU)
			dic['nameU'] = fileNameU
			uploadConfig(dic)
		else:
			print("This version is already installed - " + fileNameU)
		###########################
		if flash == 0:
			counter = 5
			while counter > 0:
				print ("Wait!!! Flashing will start up after: ")
				print (str(counter) + " sec")
				time.sleep(1)
				counter = counter - 1
			print ("START FLASHING")
			f = threading.Thread(target=flashing, args=(fileName, fileNameU, flash))
			f.daemon = True
			f.start()
			FlashingProcess(f)
			runTests()


if __name__ == "__main__":
	main()