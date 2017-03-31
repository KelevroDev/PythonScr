#!/usr/bin/python

import paramiko
import time

host = '10.67.68.67'
user = "root"
password = "root"
port = 22
#SSH connection via "paramiko"
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(host, port, user, password)
#change mode - more rights
stdin, stdout, stderr = client.exec_command("chmod +x /usr/bin/LMTest")
#change mode - more rights
stdin, stdout, stderr = client.exec_command("chmod +x /usr/bin/InputManagerTester")
time.sleep(1)
#stop InputManagerApp
stdin, stdout, stderr = client.exec_command("systemctl stop cy17_IODevices_InputManagerApp.service")
time.sleep(1)
#run InputManagerTester
stdin, stdout, stderr = client.exec_command("/usr/bin/InputManagerTester --tp=/usr/bin/Test.hbtc")
#time to execute
time.sleep(1)
#register
stdin.write("r\n")
stdin.flush()
#time to execute
time.sleep(1)
#unregister
stdin.write("u\n")
stdin.flush()
#time to execute
time.sleep(1)
#quit
stdin.write("q\n")
stdin.flush()
#time to execute
time.sleep(1)

client.close()
print ("finish")
