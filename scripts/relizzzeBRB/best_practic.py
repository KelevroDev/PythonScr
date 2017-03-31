#!/usr/bin/env python
# -*- coding: utf8 -*-
import os, time
from shutil import copyfile
import fnmatch, re
import shutil
import logging
import threading
import yaml
import paramiko
import subprocess
#from Scp import SCPClient
from os.path import isfile
from os import listdir
from os.path import join as joinpath
import serial
import sys
import win32com.client as win32
import hashlib
import datetime
#import psutil

def runTests(x):
	checkVersion(x)
	x.test_results = "Test results:\n\n"
	bin_res = bin_check(x)
	proc_res = proc_check(x)
	sys_check(x)
	SendEmail(x)

def SendEmail(x):
	print ("Sending e-mail")
	nowTime = str(datetime.datetime.now())
	emailText = "\nDate: " + nowTime
	MailHeader = "Hello,\nCY17 - SW " + version + " Has been flashed and tested." + emailText
	signature = "\n\n\nCreated by:\nE. Kiriyanov\nEKiriyanov@luxoft.com"
	outlook = win32.Dispatch('outlook.application')
	mail = outlook.CreateItem(0)
	#mail.To = 'ekiriyanov@luxoft.com; skalinina@luxoft.com; dleu@luxoft.com'
	mail.To = 'ekiriyanov@luxoft.com'
	mail.Subject = "Automated test report - CY17 sw " + x.sw_version
	mail.body = MailHeader + x.test_results + signature
	mail.send
	print ("E-mail sended" + str(nowTime))

def checkVersion(x):
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
	x.sw_version = stringVer[12:19]

	x.close()

def getRoot(FolderPass, x):
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
					x.full_path_rootfs = mypath + line
					x.name_of_rootfs = line		
		else:
			for line2 in listdir(mypath + line):#search files in next folder
				if line2.endswith('rootfs.ext3'):
					thisFileTime = os.path.getctime(mypath + line + "\\" + line2)
					if thisFileTime > maxTime:
						maxTime = thisFileTime
						x.full_path_rootfs = mypath + line + "\\" + line2#save full path to file
						x.name_of_rootfs = line2#save file name
	print ("\nFull path: ", x.full_path_rootfs)
	print ("fileName: ", x.name_of_rootfs)
	print ("Destination path - \n" + destMy)

def getUimage(FolderPass, x):
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
					x.full_path_uimage = mypath + line
					x.name_of_uimage = line
		else:
			for line2 in listdir(mypath + line):#search files in next folder
				if line2.startswith('uImage--'):
					thisFileTime = os.path.getctime(mypath + line + "\\" + line2)
					if thisFileTime > maxTime:
						maxTime = thisFileTime
						x.full_path_uimage = mypath + line + "\\" + line2#save full path to file
						x.name_of_uimage = line2#save file name
	print ("Uimage Full path: ", x.full_path_uimage)
	print ("Uimage fileName: ", x.name_of_uimage)
	print ("\nDestination path - \n" + x.dest_path)

class variables:
	configPath = "F:\\scripts\\ReadyScripts\\UploadConfig.yaml"
	f = open(configPath, 'r')
	dic = yaml.load(f)
	f.close()
	name_of_rootfs = ''
	name_of_uimage = ''
	full_path_rootfs = ''
	full_path_uimage = ''
	TestResultsBIN = ''
	TestResultsPROC = ''
	TestResultsSYS = ''
	port = dic['portIP']
	secret = dic['pass']
	user = dic['login']
	host = dic['ip']
	sw_version = ''
	percent = ''
	pathToWeekly = dic['pathWeekly']
	pathToDaily = dic['pathDaily']
	pathToEng = dic['pathEng']
	pathList = [pathToWeekly, pathToDaily, pathToEng]
	old_rootfs = dic['nameR']
	old_uimage = dic['nameU']
	dest_path = dic['pathDst']
	test_results = 'Tests were NOT performed'

def uploadConfig(x):
	f = open(configPath, "w")
	f.write(yaml.dump(x.dic, default_flow_style=False))
	f.close()

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

def FlashingProcess(f):
	print ("FlashingProcess")
	coun = 0
	while f.isAlive():
		coun = coun + 1
		print ("remaining time " + str(coun) + "\n FLASHING: PLEASE DON'T TURN OFF THE MEU!!!")
		time.sleep(5)
		os.system('cls')

#def mountUSB():

def killer():
	PROCNAME1 = "putty.exe"
	PROCNAME2 = "ttermpro.exe"
	procFind = 0
	for proc in psutil.process_iter():
	    if proc.name() == PROCNAME1:
	        proc.kill()
	        procFind = 1
	        print ("putty - killed")
	    if proc.name() == PROCNAME2:
	        proc.kill()
	        procFind = 1
	        print ("ttermpro - killed")
	if procFind == 0:
	    print ("No process COM# running")
	time.sleep(2)


def main():
	x = variables
	killer()
	mountUSB(x)
	print("START")
	print ("Getting file")
	checkPartition(x)
	flash = 0
	for i in pathList:
		rootFS = getRoot(i)
		uimage = getUimage(i)
	print ("rootfs - " + rootFS + "\nuimage - " + uimage)
	print ("rootfs - " + fileName + "\nuimage - " + fileNameU)
	#write_in_dic(x)



if __name__ == '__main__':
	main()





# TO DO:
#
#
#

