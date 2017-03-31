#!/usr/bin/python

import stat, sys, os, string, commands
import subprocess
import time

host = '10.67.68.67'#change target IP to your target IP
user = "root"
secret = "root"
port = 22

def ConnectionTime():
	ping = os.popen('ping 10.67.68.67')
	#ping = os.popen('ping www.google.com')
	result = ping.readlines()
	msLine = result[3].strip()
	#print msLine.splot(' = ')[-1]
	#print (result)
	#print ("MSLINE - " + msLine)
	#print msLine[40:41]
	if msLine == "Reply from 10.67.69.240: Destination host unreachable.":
		#print "NOK con"
		return msLine
	else:
		#print "OK con"
		return msLine
	#return msLine

def main():
	counter = 0
	reset = ''
	msLine = ConnectionTime()
	if msLine != "Reply from 10.67.69.240: Destination host unreachable.":
		while msLine != "Reply from 10.67.69.240: Destination host unreachable." and counter < 120:
			counter = counter + 1
			time.sleep(5)
			reset = "OK"
			msLine = ConnectionTime()
		print ("RESET IS - " + reset)
		return reset
	else:
		reset = "NOK"
		return reset
	print reset

if __name__ == "__main__":
	main()