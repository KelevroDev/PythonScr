#!/usr/bin/env python
# -*- coding: utf8 -*-
import sys
import os
import random
import time
import numpy as np
import math
import yaml
import urllib
from os import listdir
from os.path import isfile
from P4 import P4,P4Exception
#import copy
from os.path import join as joinpath

def Sync():
	ChangeList = input("Input ChangeList: ")
	if isfloat(ChangeList):
		path = "//CoC_System_Binaries/Packages/Public/IOController/Trunk/sys-iocontroller-bin-tr-toyota_CY17_v850/bin/sys/env/app/...@" + str(ChangeList)
		p4 = P4()
		p4.port = "172.30.89.148:3501"
		p4.user = "EKiriyanov"
		p4.password = "jatric#123"
		p4.client = "EKiriyanov_HIROP027_4022" 
		try:
			p4.connect()
			p4.run_sync(path)
			counter = 0
			while counter < 10:
				time.sleep(1)
				print "Syncing..."
				counter = counter + 1
			print "Files uploaded to Workspace: EKiriyanov_HIROP027_4022"
			p4.disconnect()
		except P4Exception:
			for e in p4.errors:
				print e
				print "ERROR -> upload"
	else:
		print "Error -> ChangeList"

def getFile(FolderPass):
	global Application1
	global Application2
	global extSize
	global uImageSize
	global uImageName
	global SW
	status = "Searching file"
	mypath = FolderPass
	print ("Check files in - %s" % (mypath))
	time.sleep(2)
	for line in listdir(mypath):#search files in folder 
		if isfile(joinpath(mypath,line)):
			if line.endswith('1.bin'):
				imageFile = mypath + line
				fileName = line
				print "\n "
				print "fileName - ", fileName
				print "imageFile - ", imageFile, (os.path.getsize(imageFile)/1024)
				Application1 = os.path.getsize(imageFile)
			if line.endswith('2.bin'):
				imageFile = mypath + line
				fileName = line
				print "\n "
				print "fileName - ", fileName
				print "imageFile - ", imageFile, (os.path.getsize(imageFile)/1024)
				Application2 = os.path.getsize(imageFile)
			if line.startswith('uImage'):
				imageFile = mypath + line
				fileName = line
				print "\n "
				print "fileName - ", fileName
				print "imageFile - ", imageFile, (os.path.getsize(imageFile)/1024)
				uImageName = fileName
				uImageSize = os.path.getsize(imageFile)
			if line.endswith('.ext3'):
				imageFile = mypath + line
				fileName = line
				print "\n "
				print "fileName - ", fileName
				print "imageFile - ", imageFile, ((os.path.getsize(imageFile)/1024)/1000)
				extSize = os.path.getsize(imageFile)
				SW = fileName

def parser():
	Application1 = 0
	Application2 = 1
	extSize = 2
	uImageSize = 3
	uImageName = ''
	SW = "A12345A"
	uImageName = "uImage--3.10.17-r0-meucy17-t101-a0-12345678901234.bin"
	f = open('E:\\FilesForTests\\update_package.xml', 'r')
	dic = f
	array = []
	for i in f:
		array.append(i)
	array[20] = "		  <size>" + extSize + "</size>\n"
	array[28] = "			<size>" + uImageSize + "</size>\n"
	array[36] = "			<size>" + Application1 + "</size>\n"
	array[44] = "			<size>" + Application2 + "</size>\n"
	array[19] = "          <filename>" + SW + "</filename>\n"
	array[27] = "            <filename>" + uImageName + "</filename>\n"
	print "20 string \'size\'", array[20]
	print "28 string \'size\'", array[28]
	print "36 string \'size\'", array[36]
	print "44 string \'size\'", array[44]
	print "19 string \'EXT3Name\'", array[19]
	print "27 string \'uImageName\'", array[27]
	f.close
	f = open('E:\\FilesForTests\\update_package.xml', 'w')
	for item in array:
		f.write(item)
	f.close

def main():
	FolderPath = raw_input("Input SW")
	pathXML = "Z:\\Weekly\\" + str(FolderPath) + "\\update_package.xml"
	Sync()
	getFile(pathXML)
	parser()

if __name__ == '__main__':
	main()
