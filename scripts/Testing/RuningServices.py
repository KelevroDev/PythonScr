#!/usr/bin/python

import paramiko
import datetime
import stat, sys, os, string, commands
import psutil
import argparse
import time
#SSH connection via "paramiko"
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname=sys.argv[1], username=sys.argv[2], password=sys.argv[3], port=int(sys.argv[4]))

logName = str(datetime.datetime.now())
filename = ("tests-results/check_running_services_" + logName+'.log')

if not os.path.exists(os.path.dirname(filename)):
    try:
        os.makedirs(os.path.dirname(filename))
    except OSError as exc: # Guard against race condition
        if exc.errno != errno.EEXIST:
            raise

runServ_str_good = "\n RuningSevices OK--------- \n\n"
runServ_str_bad = "\n RuningSevices NOK--------- \n\n" 

print ("\n\033[1;36;40m----------------------------INACTIVE SERVICES---------------------------------\033[1;m\n")

stdin, stdout, stderr = client.exec_command("systemctl list-units cy17* --state=inactive")
data = stdout.read() + stderr.read()

with open(filename, "w") as f:
    f.write("-----------INACTIVE SERVICES-----------\n\n")
    f.write(str(data))

print ("\033[1;34m" + str(data) + "\033[1;m")
print ("\n\033[1;36;40m----------------------------FAILED SERVICES---------------------------------\033[1;m\n")

stdin, stdout, stderr = client.exec_command("systemctl --state=failed")
data = stdout.read() + stderr.read()
#wright results to file
with open(filename, "a") as f:
    f.write("-----------FAILED SERVICES-----------\n\n")
    f.write(str(data))
print ("\033[1;41m" + str(data) + "\033[1;m")