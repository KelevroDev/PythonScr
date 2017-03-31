#!/usr/bin/python

import paramiko
import datetime
import stat, sys, os, string, commands
import psutil
import argparse

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname=sys.argv[1], username=sys.argv[2], password=sys.argv[3], port=int(sys.argv[4]))

stdin, stdout, stderr = client.exec_command("find /usr/bin/ *")
data = stdout.read() + stderr.read()

logName = str(datetime.datetime.now())
filename = ("tests-results/check_binary_files_" + logName+'.log')
#create folder
if not os.path.exists(os.path.dirname(filename)):
    try:
        os.makedirs(os.path.dirname(filename))
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise

f2 = open('list-of-bin.textile', 'r')

bin_str_good = "\n binaries OK--------- \n\n"
bin_str_bad = "\n binaries NOK--------- \n\n"

print ("\n\033[1;36;40m---------------------------------BINARIES---------------------------------\033[1;m\n")

for val in f2:
	if data.find(val.strip()) == -1:
		bin_str_bad = (bin_str_bad + val.strip() +'\n')
		print (val.strip() + "'\033[1;41m	- NOK\033[1;m'")
		
	else:
		bin_str_good = (bin_str_good + val.strip() +'\n')
		print (val.strip() + "'\033[1;32;40mOK\033[1;m'")

with open(filename, "w") as f:
    f.write(bin_str_good + bin_str_bad + "\n\n")


