#!/usr/bin/python

import paramiko
import time

host = '10.67.68.67'
user = "root"
password = "root"
port = 22

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(host, port, user, password)

stdin, stdout, stderr = client.exec_command("systemctl stop cy17_IODevices_InputManagerApp.service")

stdin, stdout, stderr = client.exec_command("/usr/bin/InputManagerTester --tp=/usr/bin/Test.hbtc")
time.sleep(1) 
stdin.write("r\n")
stdin.flush()
time.sleep(1)
stdin.write("u\n")
stdin.flush()
time.sleep(1)
stdin.write("q\n")
stdin.flush()
time.sleep(1)
stdin, stdout, stderr = client.exec_command("systemctl start cy17_IODevices_InputManagerApp.service")
stdin, stdout, stderr = client.exec_command("/usr/bin/InputManagerApp")
print(stdout.read().decode())



client.close()

print ("finish")
