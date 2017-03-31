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
global fileName
fileName = ''
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
global maxTime
maxTime = 0
global imageFile
global fileName
imageFile = ''
global percent
percent = 0

def getFile(FolderPass):
	status = "Searching file"
	mypath = FolderPass
	print ("Check files in - %s" % (mypath))
	time.sleep(2)
	for line in listdir(mypath):#search files in folder 
		if isfile(joinpath(mypath,line)):
			if line.endswith('.ext3'):
				thisFileTime = os.path.getctime(mypath + line)
				if thisFileTime > maxTime:
					maxTime = thisFileTime
					imageFile = mypath + line
					fileName = line
		else:
			for line2 in listdir(mypath + line):#search files in next folder
				if line2.endswith('.ext3'):
					thisFileTime = os.path.getctime(mypath + line + "\\" + line2)
					if thisFileTime > maxTime:
						maxTime = thisFileTime
						imageFile = mypath + line + "\\" + line2#save full path to file
						fileName = line2#save file name
	print ("\n\n")
	print ("Full path: ")
	print (imageFile)
	print ("fileName: ")
	print (fileName)
	print ("\n\n")

def copyFileToTarget(srcPath, destMy):
	status = "file copying"
	src = srcPath
	dest = destMy
	paramikoClient = paramiko.SSHClient()
	paramikoClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())#Open ethernet connection to MEU
	paramikoClient.connect(host, port, user, secret)
	scpClient = SCPClient(paramikoClient.get_transport())
	scpClient.put(imageFile, dest)#copy file

def progressBar(t):
	print("START PROGRESSBAR")
	time.sleep(1)
	getSize()#Destination file size
	actualSize = os.path.getsize(imageFile)#Source file size
	while t.isAlive():
		print ("Downloading...")
		getSize()
		print (swSize*1000)
		print (actualSize)
		print ("Downloaded: " + str((swSize*1000)/(actualSize/100)) + "%")#Shows the result as a percentage of download
		time.sleep(5)
		os.system('cls')
	percent = str((swSize*1000)/(actualSize/100))
	if percent == 100:
		print "Correct SIZE"
	else:
		print "Incorrect SIZE"
	count = 120
	while count > 0:#Time for cleaning buffer
		time.sleep(1)
		count = count - 1
		print "Wait - " + str(counter)
	print ("DONE")
	print ("Flie " + imageFile + " on target!!!")
	print ("Starting flashing")

def copyToUSB():
	paramikoClient = paramiko.SSHClient()
	paramikoClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	paramikoClient.connect(host, port, user, secret)
	scpClient = SCPClient(paramikoClient.get_transport())
	scpClient.put(srcPath, "/tmp/")
	scpClient.close()
	paramikoClient.close()

def checkVersion():
	print ("Check Version")
	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect(hostname=host, username=user, password=secret, port=int(port))
	stdin, stdout, stderr = client.exec_command("cat /etc/Toyota_CY17.XML | grep '<Filename>A'")
	data = stdout.read() + stderr.read()
	stringVer = str(data)
	print ("Version is %s *** *** ***" % stringVer)
	return stringVer

def getSize():
	print ("Getting SIZE")
	paramikoClient = paramiko.SSHClient()
	paramikoClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	paramikoClient.connect(host, port, user, secret)
	stdin, stdout, stderr = paramikoClient.exec_command("ls -s /mnt/*" + fileName + "*")
	data = stdout.read() + stderr.read()
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

def checkPartition():
	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect(hostname=host, username=user, password=secret, port=int(port))
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
		print ('PARTITION - 6***************************')
	if line.startswith("/dev/mmcblk0p8"):
		part = 8
		return part
		print ('PARTITION - 8***************************')
	else:
		print ("Can't find patition")
	print ("___Current__PARTITION is " + str(part) + "______")
	client.close()

def flashing():
	x = SerialConnection("COM9", "115200")
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
	print ("STARTING REBOOT")
	x.run("reboot -f")
	counter = 30
	while counter > 0: 
		time.sleep(1)
		print "Wait till rebooting " + str(counter)
		counter = counter - 1
	x.run("root")
	time.sleep(1)
	x.run("root")
	time.sleep(1)
	print ("ETHERNET CONNECTION")
	x.run("udhcpc -i eth0")
	time.sleep(5)
	checkPartition()
	time.sleep(2)
	x.run("version")
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
	client.close()

def bin_check():
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
	print ("---------------------------------BINARIES---------------------------------")
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

def checkVersion():
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
	proc_str_good = "\n processes OK--------- \n\n"
	proc_str_bad = "\n processes NOK--------- \n\n"
	stdin, stdout, stderr = client.exec_command("ps")
	data = stdout.read() + stderr.read()
	print ("---------------------------------PROCESSES---------------------------------")
	for val in f2:
		if data.find(val.strip()) == -1:
			proc_str_bad = (proc_str_bad + val.strip() +'\n')
			print (val.strip() + "	- NOK")
		else:
			proc_str_good = (proc_str_good + val.strip() +'\n')
			print (val.strip() + " OK")
	TestResultsPROC = (proc_str_good + proc_str_bad + "\n\n")
	return TestResultsPROC
	client.close()

def SendEmail():
	print ("Sending e-mail")
	nowTime = str(datetime.datetime.now())
	emailText = "\nDate: " + nowTime
	MailHeader = "Hello,\nCY17 - SW " + version + " was flashed and tested." + emailText
	signature = "\n\n\nCreated by:\nE. Kiriyanov\nEKiriyanov@luxoft.com"
	outlook = win32.Dispatch('outlook.application')
	mail = outlook.CreateItem(0)
	mail.To = 'ekiriyanov@luxoft.com'
	mail.Subject = "Automated test report - CY17 sw " + version
	mail.body = MailHeader + conn + TestResultsBIN + TestResultsPROC + TestResultsSYS + signature
	mail.send
	print ("E-mail sended")
	client.close()

def sys_check():
	global TestResultsSYS
	TestResultsSYS = 'Services '
	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect(hostname=host, username=user, password=secret, port=int(port))
	stdin, stdout, stderr = client.exec_command("ls -l /lib/systemd/system")
	data = stdout.read() + stderr.read()
	logName = str(datetime.datetime.now())
	f2 = open('D:\Automation\flashing\scripts\Testing\list-of-serv.textile', 'r')
	serv_str_good = "\n services OK-------- \n\n"
	serv_str_bad = "\n services NOK-------- \n\n"
	print ("---------------------------------SERVICES---------------------------------\033[1;m")
	for val in f2:
		if data.find(val.strip()) == -1:
			serv_str_bad = (serv_str_bad + val.strip() +'\n')
			print (val.strip() + "	- NOK")
		else:
			serv_str_good = (serv_str_good + val.strip() +'\n')
			print (val.strip() + "	- OK")
	TestResultsSYS = (serv_str_good + serv_str_bad + "\n\n")
	return TestResultsSYS
	client.close()

def Connection():
	ping = os.popen('ping 10.67.68.67')
	result = ping.readlines()
	msLine = result[3].strip()
	print (result)
	print ("MSLINE - " + msLine)
	print msLine[40:41]
	if msLine == "Reply from 10.67.69.240: Destination host unreachable.":
		print "NOK"
	else:
		print "OK"
	return msLine

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
	x.run("root")
	time.sleep(2)
	x.run("mount /dev/sda1 /mnt/")
	time.sleep(2)
	x.run("udhcpc -i eth0")
	time.sleep(2)
	x.close()

def runTests():
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
		getFile(i)
	t = threading.Thread(target=copyFileToTarget, args=(imageFile, destMy))
	t.daemon = True
	t.start()
	percent = progressBar(t)
	counter = 5
	while counter > 0:
		print ("Wait!!! Flashing started up after: ")
		print (str(counter) + " sec")
		time.sleep(1)
		counter = counter - 1
	if percent == 100:
		flashing()
	else:
		print "The file is downloaded incorrectly!!!"
		print "Start to download the file again!!!"
		counter = 0
		while percent != 100:
			if counter < 3:
				t = threading.Thread(target=copyFileToTarget, args=(imageFile, destMy))
				t.daemon = True
				t.start()
				progressBar(t)
				if percent == 100:
					counter = 5
					flashing()
				else:
					counter = counter + 1
				print str(counter) + " attempts to download a file"
			else:
				print "Problems with downloading!!!"
				print "Please check source file and try again"
				break
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