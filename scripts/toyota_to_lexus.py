#!/usr/bin/python

import datetime
import stat, sys, os, string, commands
import subprocess
import time
import paramiko
import psutil
import argparse
from collections import deque

host = '10.67.68.67'#change target IP to your target IP
user = "root"
secret = "root"
port = 22

servicePath1 = "/lib/systemd/system/cy17_car_variant_env"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname=host, username=user, password=secret, port=int(port))

stdin, stdout, stderr = client.exec_command("cat " + servicePath1)
data = stdout.read() + stderr.read()

new_Lexus = "MAKE_OF_CAR=LEXUS"
new_Toyota = "MAKE_OF_CAR=TOYOTA"
#check DCU state
if new_Lexus in data:
	print ("\033[1;36;40m\nNow is -  " + "LEXUS" + "\n\033[1;m")
if new_Toyota in data:
	print ("\033[1;36;40m\nNow is -  " + "TOYOTA" + "\n\033[1;m")

print ("Wait, we Change DCU state...")

stdin, stdout, stderr = client.exec_command("cat " + servicePath1)#read file
data = stdout.read() + stderr.read()

if new_Lexus in data:
	stdin, stdout, stderr = client.exec_command("cp /dev/null " + servicePath1)
	time.sleep(0.5)
	stdin, stdout, stderr = client.exec_command("printf '%s\n' " + new_Toyota + " >> " + servicePath1)
	data = stdout.read() + stderr.read()
if new_Toyota in data:
	stdin, stdout, stderr = client.exec_command("cp /dev/null " + servicePath1)
	time.sleep(0.5)
	stdin, stdout, stderr = client.exec_command("printf '%s\n' " + new_Lexus + " >> " + servicePath1)
	data = stdout.read() + stderr.read()

stdin, stdout, stderr = client.exec_command("cat " + servicePath1)
data = stdout.read() + stderr.read()

if new_Lexus in data:#type new DCU state
	print ("\n\033[1;32;40mNow is " + "LEXUS" + "\n\033[1;m")
elif new_Toyota in data:
	print ("\n\033[1;32;40mNow is " + "TOYOTA" + "\n\033[1;m")
else:
	print ("\033[1;41mERROR\033[1;m")

print ("Done")