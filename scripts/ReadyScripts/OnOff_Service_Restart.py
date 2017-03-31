#!/usr/bin/python

import paramiko
import datetime
import stat, sys, os, string, commands
import psutil
import argparse
import time

configPath = "D:\\Automation\\flashing\\scripts\\UploadConfig.yaml"
f = open(configPath, 'r')
dic = yaml.load(f)
f.close()

global host
host = dic['ip']
global user
user = dic['login']
global secret
secret = dic['pass']
global port
port = dic['portIP']


def OnOff_Restart():
	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect(hostname=host, username=user, password=secret, port=int(port))

	stdin, stdout, stderr = client.exec_command("journalctl | grep -i restart")
	data = stdout.read() + stderr.read()
	Restart = ("\nOnOff\nRestart Services: \n", data)
	return Restart

def OnOff_DateTime():
	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect(hostname=host, username=user, password=secret, port=int(port))

	stdin, stdout, stderr = client.exec_command("date")
	data = stdout.read() + stderr.read()
	dataTime = ("\nOnOff\nDate & time on Meu: ", data)
	return dataTime

def copyFileToTarget(srcPath, destMy):
	File = srcPath
	status = "file copying"
	src = srcPath
	dest = destMy
	paramikoClient = paramiko.SSHClient()
	paramikoClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	paramikoClient.connect(host, port, user, secret)
	scpClient = SCPClient(paramikoClient.get_transport())
	print "srcPath " + imageFile
	print "destMy " + dest
	scpClient.put(File, dest)
	count = 0
	while count < 5:
		print ("COUNT " + str(count))
		time.sleep(1)
		count = count + 1
	paramikoClient.close()

def WebDav():
	src = '/mnt/File.file'
	dest = '/DCU/File.file'
	kill = ("rm", dest)
	copyFileToTarget(src, dest)
	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect(hostname=host, username=user, password=secret, port=int(port))
	stdin, stdout, stderr = client.exec_command("ls")
	File_here_data = stdout.read() + stderr.read()
	stdin, stdout, stderr = client.exec_command(kill)
	file_killed_data = stdout.read() + stderr.read()
	out_put_killer = ("Present file: LS", File_here_data, "\nAfter removal, the file is missing: LS", file_killed_data)









def main():
	outputOnOff = OnOff_Restart()
	return outputOnOff


if __name__ == "__main__":
	main()

