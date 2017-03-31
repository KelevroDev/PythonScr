import win32api
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



def DiskCheck():
	drives = win32api.GetLogicalDriveStrings()
	drives = drives.split('\000')[:-1]
	print "drives"
	print drives
	counter = 1
	for disk in drives:
		print "Disk "+ str(counter) + " -> " + disk
		counter = counter + 1
	return drives

def inside():
	drives = DiskCheck()
	size = 0
	for drive in drives:
		print drive
		for dirpath, dirnames, filenames in os.walk(drive):
			for filename in [f for f in filenames if f.endswith(".jpg" or ".jpeg")]:
				path = os.path.join(dirpath, filename)
				#dest = "E:\ZTEST-TEST" # path to USB
				#print os.path.join(path)
				#size = size + os.path.getsize(path)
				#shutil.copy(path, "E:\ZTEST-TEST")
	print size
	return size


def main():
	#DiskCheck()
	inside()
	print "DONE!!!"

if __name__ == "__main__":
	main()