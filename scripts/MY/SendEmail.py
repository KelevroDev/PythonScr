import win32com.client as win32
import datetime
import paramiko
import datetime
import stat, sys, os, string, commands
#import psutil
import argparse

global version
version = 'Version '
global TestResultsBIN
TestResultsBIN = 'Binaries \n'
global TestResultsPROC
TestResultsPROC = 'Process \n'
global TestResultsSYS
TestResultsSYS = 'Services \n'
global conn
conn = "\n NO CONNECTION \n"


def bin_check():
	global TestResultsBIN
	TestResultsBIN = 'Binaries \n'
	host = '10.67.68.25'
	user = "root"
	secret = "root"
	port = 22
	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect(hostname=host, username=user, password=secret, port=int(port))
	stdin, stdout, stderr = client.exec_command("find /usr/bin/ *")
	data = stdout.read() + stderr.read()
	f2 = open('E:\scripts\list-of-bin.textile', 'r')
	bin_str_good = "\n binaries OK--------- \n\n"
	bin_str_bad = "\n binaries NOK--------- \n\n"
	print ("---------------------------------BINARIES---------------------------------")
	for val in f2:
		if data.find(val.strip()) == -1:
			bin_str_bad = (bin_str_bad + val.strip() +'\n')
			print (val.strip() + "	- NOK")
		else:
			bin_str_good = (bin_str_good + val.strip() +'\n')
			print (val.strip() + "	- OK")
	TestResultsBIN = "\n\n" + bin_str_good + bin_str_bad + "\n\n"
	print TestResultsBIN
	return TestResultsBIN

def checkVersion():
	global version
	version = 'Version '
	print ("Check Version")
	host = '10.67.68.25'
	user = "root"
	secret = "root"
	port = 22
	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect(hostname=host, username=user, password=secret, port=int(port))
	#take a vesion
	stdin, stdout, stderr = client.exec_command("cat /etc/Toyota_CY17.XML | grep '<Filename>A'")
	data = stdout.read() + stderr.read()
	stringVer = str(data)
	print (stringVer)
	version = stringVer[12:19]
	return version

def proc_check():
	global TestResultsPROC
	TestResultsPROC = 'Process '
	host = '10.67.68.25'
	user = "root"
	secret = "root"
	port = 22
	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect(hostname=host, username=user, password=secret, port=int(port))
	stdin, stdout, stderr = client.exec_command("ps /lib/systemd/system")
	data = stdout.read() + stderr.read()
	logName = str(datetime.datetime.now())
	f2 = open('E:\scripts\Testing\list-of-process.textile','r')
	proc_str_good = "\n processes OK--------- \n\n"
	proc_str_bad = "\n processes NOK--------- \n\n"
	stdin, stdout, stderr = client.exec_command("ps")
	data = stdout.read() + stderr.read()
	print ("---------------------------------PROCESSES---------------------------------")
	for val in f2:
		if data.find(val.strip()) == -1:
			proc_str_bad = (proc_str_bad + val.strip() +'\n')
			print (val.strip() + "	- NOK")
		else:
			proc_str_good = (proc_str_good + val.strip() +'\n')
			print (val.strip() + " OK")
	TestResultsPROC = (proc_str_good + proc_str_bad + "\n\n")
	return TestResultsPROC

def SendEmail():
	print ("Sending e-mail")
	#conn = "\nCONNECTION is UP\n"
	nowTime = str(datetime.datetime.now())
	emailText = "\nDate: " + nowTime
	MailHeader = "Hello,\nCY17 - SW " + version + " was flashed and tested." + emailText
	signature = "\n\n\nCreated by:\nE. Kiriyanov\nEKiriyanov@luxoft.com"
	#TestResults = "\n\nSome results - OK\nSome results - OK\nSome results - NOK\nSome results - OK\n...\n..."
	outlook = win32.Dispatch('outlook.application')
	mail = outlook.CreateItem(0)
	mail.To = 'ekiriyanov@luxoft.com'
	mail.Subject = "Automated test report - CY17 sw " + version
	mail.body = MailHeader + conn + TestResultsBIN + TestResultsPROC + TestResultsSYS + signature
	mail.send
	print ("E-mail sended")

def sys_check():
	global TestResultsSYS
	TestResultsSYS = 'Services '
	host = '10.67.68.25'
	user = "root"
	secret = "root"
	port = 22
	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect(hostname=host, username=user, password=secret, port=int(port))
	stdin, stdout, stderr = client.exec_command("ls -l /lib/systemd/system")
	data = stdout.read() + stderr.read()
	logName = str(datetime.datetime.now())
	f2 = open('E:\scripts\Testing\list-of-serv.textile', 'r')
	serv_str_good = "\n services OK-------- \n\n"
	serv_str_bad = "\n services NOK-------- \n\n"
	print ("---------------------------------SERVICES---------------------------------")
	for val in f2:
		if data.find(val.strip()) == -1:
			serv_str_bad = (serv_str_bad + val.strip() +'\n')
			print (val.strip() + "	- NOK")
		else:
			serv_str_good = (serv_str_good + val.strip() +'\n')
			print (val.strip() + " OK")
	TestResultsSYS = (serv_str_good + serv_str_bad + "\n\n")
	return TestResultsSYS

#"Packets: Sent = 4, Received = 4, Lost = 0 (0% loss),"
def Connection():
	ping = os.popen('ping 10.67.68.25')
	#ping = os.popen('ping www.google.com')
	result = ping.readlines()
	msLine = result[3].strip()
	#print msLine.splot(' = ')[-1]
	print (result)
	print ("MSLINE - " + msLine)
	print msLine[40:41]
	if msLine == "Reply from 10.67.25.240: Destination host unreachable.":
		print "NOK"
	else:
		print "OK"
	#return str(msLine[40:41])
	return msLine

def main():
	res = Connection()
	print "res - "
	print (res)
	if res == "Reply from 10.67.25.240: Destination host unreachable.":
		print 'Connection failed!'
		SendEmail()
	else:
		checkVersion()
		bin_res = bin_check()
		proc_res = proc_check()
		sys_check()
		SendEmail()

#Connection()
if __name__ == "__main__":
	main()
