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


configPath = "F:\\scripts\\ReadyScripts\\UploadConfig.yaml"
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


def flashing():
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
		x.run("dd if=/mnt/" + fileNameU + " of=/dev/mmcblk0p5")
		#time.sleep(900)
		x.run("umount /mnt")
		x.run("echo -e \\\\x01\\\\x00\\\\x01\\\\x01 > /dev/mmcblk0p2")#Start from 6 partition
		x.run("sync")
	if p == 6:
		print ("---- flashing 8 part ----")
		print ("RootFS File name - " + fileName)
		print ("uImage File name - " + fileNameU)
		x.run("dd if=/mnt/" + fileName + " of=/dev/mmcblk0p8")
		x.run("dd if=/mnt/" + fileNameU + " of=/dev/mmcblk0p7")
		#time.sleep(900)                    of=/dev/mmcblk0p...
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
	print ("\n\n")
	print ("Full path: ")
	print (imageFile)
	print ("fileName: ")
	print (fileName)
	print ("\n\n")
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
					fileName = line
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

def progressBar(t):# Show actual progress bar(%)
	print ("FileName - " + imageFile)
	count = 0
	print("START PROGRESSBAR")
	time.sleep(5)
	print ("FROM -> " + str(imageFile))
	print ("TO -> "+ str(destMy + fileName))
	while t.isAlive():
		print ("Downloading...")
		print ("FROM -> " + str(imageFile))
		print ("TO   -> " + str(destMy + "\\" + fileName))
		print (" It took -> " + str(count) + " <- seconds ")
		count = count + 5 
		time.sleep(5)
		os.system('cls')
	print ("DONE")
	print ("Flie " + fileName + " on target!!!")

def copyFileToTarget(srcPath, destMy): # TO PC, NOT HARDWARE
	from shutil import copyfile
	srcfile = srcPath
	dstdir = destMy
	copyfile(srcfile, dstdir)
	print ("srcPath " + srcfile)
	print ("destMy " + dstdir)

def main():
	for i in pathList:
		rootFS = getRoot(i)
		uimage = getUimage(i)
	print ("rootfs - " + rootFS + "\nuimage - " + uimage)
	print ("rootfs - " + fileName + "\nuimage - " + fileNameU)
	
	print (destMy)
	if nameR != fileName:
		destMyRoot = destMy + fileName
		t = threading.Thread(target=copyFileToTarget, args=(imageFile, destMyRoot))
		t.daemon = True
		t.start()
		progressBar(t)
		dic['nameR'] = fileName

		uploadConfig(dic)
	else:
		print("This version is already installed - " + fileName)

	if nameU != fileNameU:
		destMyUimage = destMy + fileNameU
		b = threading.Thread(target=copyFileToTarget, args=(imageFileU, destMyUimage))
		b.daemon = True
		b.start()
		progressBar(b)
		dic['nameU'] = fileNameU
		uploadConfig(dic)
	else:
		print("This version is already installed - " + fileNameU)

	



main()