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

#######################################################################################
#                                                                                     #
#                                                                                     #
#                                                                                     #
# Configure "UploadConfig.yaml": Input path Destination for new image                 #
#                                                                                     #
# Configure "UploadConfig.yaml": Input path to Source file                            #
#                                                                                     #
#                                                                                     #
#                                                                                     #
#######################################################################################

configPath = "E:\\scripts\\ReadyScripts\\UploadConfig.yaml"# Change path to config file

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
destMy = dic['pathForAll']
#destMy = dic['pathDst']
global host
host = dic['ip']
global user
user = dic['login']
global secret
secret = dic['pass']
global port
port = dic['portIP']
global stringVer
stringVer = ''
global status
status = ""
global maxTime
global percent
percent = 0# By defoult

def getFile(FolderPass):# Get the path of latest image
	global fileName
	global imageFile
	global maxTime
	maxTime = 0
	status = "Searching file"
	mypath = FolderPass
	print ("Check files in - %s" % (mypath))
	time.sleep(2)
	for line in listdir(mypath):# Search files in folder 
		if isfile(joinpath(mypath,line)):
			if line.startswith('uImage'):
				thisFileTime = os.path.getctime(mypath + line)
				if thisFileTime > maxTime:
					maxTime = thisFileTime
					imageFile = mypath + line
					fileName = line
		else:
			for line2 in listdir(mypath + line): #search files in next folder
				if line2.startswith('uImage'):
					thisFileTime = os.path.getctime(mypath + line + "\\" + line2)
					if thisFileTime > maxTime:
						maxTime = thisFileTime
						imageFile = mypath + line + "\\" + line2 # Save full path to file
						fileName = line2 # Save file name
	print ("\n\n")
	print ("Full path: ")
	print (imageFile)
	print ("fileName: ")
	print (fileName)
	print ("\n\n")
	print ("Destination path - \n" + destMy)

def copyFileToTarget(srcPath, destMy): # Copy new image to your PC
	srcfile = srcPath
	dstdir = destMy
	shutil.copy(srcfile, dstdir)
	print "srcPath " + imageFile
	print "destMy " + destMy

def progressBar(t):# Show actual progress bar(%)
	print ("FileName - " + imageFile)
	print("START PROGRESSBAR")
	time.sleep(5)
	actualSize = os.path.getsize(imageFile)# Source file size
	print ("FROM -> " + str(imageFile))
	swSize = os.path.getsize(destMy + fileName)# Dest file
	print ("TO -> "+ str(destMy + fileName))
	while t.isAlive():
		print ("Downloading...")
		swSize = os.path.getsize(destMy + "\\" + fileName)
		print (swSize)
		print (actualSize)
		print ("FROM -> " + str(imageFile))
		print ("TO   -> " + str(destMy + "\\" + fileName))
		print ("Downloaded: " + str((swSize*100)/(actualSize)) + " %")# Shows the result as a percentage of download
		time.sleep(5)
		os.system('cls')
	print ("Actual size - ", actualSize)
	print ("DONE")
	print ("Flie " + imageFile + " on target!!!")

def SendEmail():#Send eMail with/without test results
	print ("Sending e-mail")
	nowTime = str(datetime.datetime.now())
	emailText = "\nDate: " + nowTime
	MailHeader = "Hello,\nCY17 - new Image was downloaded." + emailText
	signature = "\n\n\nCreated by:\nE. Kiriyanov\nEKiriyanov@luxoft.com"
	outlook = win32.Dispatch('outlook.application')
	mail = outlook.CreateItem(0)
	mail.To = 'ekiriyanov@luxoft.com; skalinina@luxoft.com'#insert email recipients
	mail.Subject = "File downloaded " + fileName
	mail.body = "File \"" + str(imageFile) + "\"   on local PC \n -> " + nowTime + "\n ->" + signature 
	mail.send
	print ("E-mail sended")

def main():
	for i in pathList:
		getFile(i)
	print "FILE FOR FLASHING - " + imageFile
	time.sleep(5)
	t = threading.Thread(target=copyFileToTarget, args=(imageFile, destMy))
	t.daemon = True
	t.start()
	progressBar(t)
	print ("File downloaded")
	SendEmail()

if __name__ == "__main__":
	main()