import paramiko
import datetime
import stat, sys, os, string, commands
import psutil
import argparse


# what if sys.argv has less than 5 parameters or some of them are missed? Here should be a check
"""
if len(sys.argv) == 5:
	# ok we can continue
	host = sys.argv[1]
	user = sys.argv[2]
	secret = sys.argv[3]
	port = sys.argv[4]

else:
	# show error message
	print("ERROR: invalid argument count")

"""


host = sys.argv[1]
user = sys.argv[2]
secret = sys.argv[3]
port = sys.argv[4]



client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname=host, username=user, password=secret, port=int(port))

stdin, stdout, stderr = client.exec_command("find /usr/bin/ *")
data = stdout.read() + stderr.read()


logName = str(datetime.datetime.now()) # this doesn't work for windows os because it contains forbidden symbols

f1 = open("binaries" + logName+'.txt', "w")	# 
f2 = open('list-of-bin.textile', 'r')

"""
Here should be "try except" blocks (or "with ... as") to prevent situations than 
files can't be created or opened.
In "except" block must be proper error message.

Than we have a deal with strings, I think there are no reasons to use expressions 
like this: "binaries" + logName+'.txt'
String formating is exactly that we need in this case: "binaries%s.txt" % logName
"""

# try to use one coding style. At code above you use camel case and here underscore separators.
bin_str_good = "\n binaries OK--------- \n\n"
bin_str_bad = "\n binaries NOK--------- \n\n"

print ("---------------------------------BINARIES---------------------------------")


print (val.strip() + "'\033[1;41m	- NOK\033[1;m'") - such line looks really awful. Reasons:
#1. using "+" instead of string formating
#2. does it comfortable for you to use raw ANSI code every time than you need colored message? 
#Also this is unnamed constant value.
#If you need colored output in your script just write proper class/functions and use 
#it/them in every script there you have such needs. Something like this:

from colorama import init 	# for windows only
init()						# for windows only


class ConsoleMessage:
    @staticmethod
    def normal(text):
        print(text)

    @staticmethod
    def blue(text):
        print("\033[94m%s\033[0m" % text)

    @staticmethod
    def yellow(text):
        print("\033[93m%s\033[0m" % text)

    @staticmethod
    def red(text):
        print("\033[91m%s\033[0m" % text)

    @staticmethod
    def purple(text):
        print("\033[95m%s\033[0m" % text)

    @staticmethod
    def green(text):
        print("\033[92m%s\033[0m" % text)



for val in f2:
	if data.find(val.strip()) == -1:
		bin_str_bad = (bin_str_bad + val.strip() +'\n')
		print (val.strip() + "'\033[1;41m	- NOK\033[1;m'")
		#print '\033[1;41m	- NOK\033[1;m'
		
	else:
		bin_str_good = (bin_str_good + val.strip() +'\n')
		print (val.strip() + "	- OK")

f1.write("\n\n" + bin_str_good + bin_str_bad + "\n\n")


# I'm not sure that there should be so many "\n" but this is up to you
