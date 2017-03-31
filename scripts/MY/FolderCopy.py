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

configPath = "D:\\old_PC\\scripts\MY\\UploadConfig.yaml"# Change path to config file

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
#global destMy
destMy = dic['pathDst']
#destMy = "Y:\\Engineering\\"
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
global imageFile
imageFile = ''
global thisFolderTime
percent = 0# By defoult

def getFile(FolderPass):# Get the path of latest image
	global fileName
	#global imageFile
	global maxTime
	maxTime = 0
	status = "Searching file"
	mypath = FolderPass
	print ("Check files in - %s" % (mypath))
	time.sleep(2)
	for line in listdir(mypath):# Search ffolder in folder 
		if os.path.isdir(joinpath(mypath,line)):
			print ("- ")
			thisFolderTime = os.path.getctime(mypath + line)
			if thisFolderTime > maxTime:
				maxTime = thisFolderTime
				imageFile = mypath + line
				fileName = line
				print (fileName)
				print (imageFile)
	print ("\n\n")
	print ("Full path: ")
	print (imageFile)
	print ("fileName: ")
	print (fileName)
	print ("\n\n")
	print ("Destination path - \n" + destMy)
	return imageFile

def copyFileToTarget(srcPath, destMy, d): # Copy new image to your PC
	srcfile = srcPath
	dstdir = destMy
	try:
		shutil.copytree(srcfile, dstdir, symlinks=False, ignore=None)
		d.dataR = "File \"" + str(srcfile) + "\"   on shared folder \n -> " + dstdir + "\n"
	except:
		d.dataR = "alredy copied"
		print ("alredy copied")

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

def SendEmail(d):#Send eMail with/without test results
	print ("Sending e-mail")
	nowTime = str(datetime.datetime.now())
	emailText = "\nDate: " + nowTime
	MailHeader = "Hello,\nCY17 - new Image was downloaded." + emailText
	signature = "\n\n\nCreated by:\nE. Kiriyanov - The Best of the Best\nEKiriyanov@luxoft.com"
	outlook = win32.Dispatch('outlook.application')
	mail = outlook.CreateItem(0)
	mail.To = 'ekiriyanov@luxoft.com' #skalinina@luxoft.com'#insert email recipients
	mail.Subject = "File downloaded " + fileName
	#mail.body = "File \"" + str(fileName) + "\"   on shared folder \n -> " + nowTime + "\n ->" + signature 
	mail.body = d.dataR + "\n" + signature
	mail.send
	print ("E-mail sended")

class data():
	dataR = ''

def main():
	pathDst = "D:\\NewImagesDownload\\"
	imageFile = getFile("Y:\\Engineering\\")
	print ("FILE FOR FLASHING - " + imageFile)
	time.sleep(5)
	print ("DEST MY")
	destMy = pathDst + fileName + "\\"
	print (destMy)
	d = data()
	t = threading.Thread(target=copyFileToTarget, args=(imageFile, destMy, d))
	t.daemon = True
	t.start()
	progressBar(t)
	SendEmail(d)

if __name__ == "__main__":
	main()