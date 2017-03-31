#!/usr/bin/python

import datetime
import stat, sys, os, string, commands
import subprocess
import time
import paramiko

#change target IP to your target IP
host = '10.67.68.67'
user = "root"
secret = "root"
port = 22

ser = "python service_check_script.py" + ' ' + str(host) + ' ' + str(user) + ' ' + str(secret) + ' ' + str(port)
proc = "python proc_check_script.py" + ' ' + str(host) + ' ' + str(user) + ' ' + str(secret) + ' ' + str(port)
binaries = "python bin_check_script.py" + ' ' + str(host) + ' ' + str(user) + ' ' + str(secret) + ' ' + str(port)
wifi = "python WiFi_Ping_Google.py" + ' ' + str(host) + ' ' + str(user) + ' ' + str(secret) + ' ' + str(port)
runServ = "python RuningServices.py" + ' ' + str(host) + ' ' + str(user) + ' ' + str(secret) + ' ' + str(port)
#add tests if you need
ListTests = [ser, proc, binaries, runServ, wifi]
#checking connection
response = os.system("ping -c 1 " + host)
#256 - no connection
if str(response) != "256":
	print '\033[1;32;40mConnectioin is up!\033[1;m'
	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect(hostname=host, username=user, password=secret, port=int(port))
	#take a vesion
	stdin, stdout, stderr = client.exec_command("cat /etc/Toyota_CY17.XML | grep '<Filename>A'")
	data = stdout.read() + stderr.read()
	stringVer = str(data)
	servicePath1 = "/lib/systemd/system/cy17_HMI_HMI.service"
	string1 = "MAKE_OF_CAR=LEXUS"
	string2 = "MAKE_OF_CAR=TOYOTA"
	#check which car on board
	stdin, stdout, stderr = client.exec_command("cat /lib/systemd/system/cy17_car_variant_env")
	data = stdout.read() + stderr.read()
	filename = ''
	logName = str(datetime.datetime.now())
	#show message *car & version*
	if string1 in data:
		filename = "\033[1;32;40m			  tests_for_" + "L2_" + stringVer[12:19] +'\033[1;m'
	if string2 in data:
		filename = "\033[1;32;40m			  tests_for_" + "T2_" + stringVer[12:19] +'\033[1;m'
	#run tests
	print filename
	for elem in ListTests:
		time.sleep(2)
		subprocess.Popen(elem, shell=True)
else:
	print '\033[1;41mConnectioin is down!\033[1;m'