#!/usr/bin/env python

import os
import datetime
import time

text = """#!/usr/bin/env python
import os


def y():
	print ("FUCK YEAH!!!")

#main()

 """
print ("WTF")
f = open("F:/scripts/MY/zzz.py", "w")

f.write(text)
f.close

time.sleep (2)

def x():
	import zzz
	zzz.y()

x()