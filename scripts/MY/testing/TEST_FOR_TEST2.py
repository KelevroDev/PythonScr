#!/usr/bin/env python

import os
import datetime
import time
import threading
import runscript
import sys
import subprocess
#import zzz
someText = "\"WTF, Boo\""

text = """#!/usr/bin/env python
import os

def y():
	text = """ + someText + """
	f = open("F:/scripts/MY/testing/aaa.txt", "w")
	f.write(text)
	f.close
	print("DONE")

y()
#main()

 """

def createF():
	print ("WTF")
	f = open("F:/scripts/MY/testing/zzz.py", "w")
	f.write(text)
	f.close

f = threading.Thread(target=createF)
f.daemon = True
f.start()

time.sleep (2)

def x():
	subprocess.call("python F:/scripts/MY/testing/zzz.py")

x()