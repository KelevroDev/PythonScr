#!/usr/bin/python

import paramiko
import datetime
import stat, sys, os, string, commands
import psutil
import time

#change target IP to your target IP 
host = '10.67.68.67'
user = "root"
secret = "root"
port = 22
#SSH connection via "paramiko"
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname=host, username=user, password=secret, port=int(port))

#check file
stdin, stdout, stderr = client.exec_command("ls /usr/bin")
data = stdout.read() + stderr.read()
if data.find("LMTest") == -1:
	print ("\033[1;41mPlease put LMTest binary to /usr/bin!!!\033[1;m")
else :
	stdin, stdout, stderr = client.exec_command("chmod +x LMTest")
	print ("'\033[1;32;40mLMTest start running\033[1;m")

#stop HMI
stdin, stdout, stderr = client.exec_command("systemctl stop cy17_HMI_HMI")
data = stdout.read() + stderr.read()
time.sleep(2)
print ("HMI - stopped")

#stop IODevices_AppController
stdin, stdout, stderr = client.exec_command("systemctl stop cy17_IODevices_AppController")
data = stdout.read() + stderr.read()
time.sleep(2)
print ("AppController - stopped")

#start IODevices_AppController
stdin, stdout, stderr = client.exec_command("systemctl start cy17_IODevices_AppController")
data = stdout.read() + stderr.read()
time.sleep(2)

#check process
stdin, stdout, stderr = client.exec_command("ps")
data = stdout.read() + stderr.read()

if data.find("AppController") == -1:
	print ("\033[1;41mAppController - not started!!!\033[1;m")
else :
	print ("'\033[1;32;40mAppController - started\033[1;m")
#run LMTest
stdin, stdout, stderr = client.exec_command("chmod +x /usr/bin/LMTest")
time.sleep(1)
stdin, stdout, stderr = client.exec_command("/usr/bin/LMTest")
#data = stdout.read() + stderr.read()
#stdin.flush()
client.close()
print ("finish")