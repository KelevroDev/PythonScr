#!/usr/bin/python

import paramiko
import datetime
import stat, sys, os, string, commands
import psutil
import argparse
#SSH connection via "paramiko"
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname=sys.argv[1], username=sys.argv[2], password=sys.argv[3], port=int(sys.argv[4]))
stdin, stdout, stderr = client.exec_command("ps /lib/systemd/system")
data = stdout.read() + stderr.read()
logName = str(datetime.datetime.now())
filename = ("tests-results/check_running_processes_" + logName+'.log')
if not os.path.exists(os.path.dirname(filename)):
    try:
        os.makedirs(os.path.dirname(filename))
    except OSError as exc: # Guard against race condition
        if exc.errno != errno.EEXIST:
            raise
f2 = open('list-of-process.textile','r')
proc_str_good = "\n processes OK--------- \n\n"
proc_str_bad = "\n processes NOK--------- \n\n"
stdin, stdout, stderr = client.exec_command("ps")
data = stdout.read() + stderr.read()
print ("\033[1;36;40m---------------------------------PROCESSES---------------------------------\033[1;m")
for val in f2:
	if data.find(val.strip()) == -1:
		proc_str_bad = (proc_str_bad + val.strip() +'\n')
		print (val.strip() + "'\033[1;41m	- NOK\033[1;m'")
	else:
		proc_str_good = (proc_str_good + val.strip() +'\n')
		print (val.strip() + "'\033[1;32;40mOK\033[1;m'")
with open(filename, "w") as f:
    f.write(proc_str_good + proc_str_bad + "\n\n")