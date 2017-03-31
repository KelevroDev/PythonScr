#!/usr/bin/env python
# -*- coding: utf8 -*-

import time
import os

def ShowProgressBar():
	counter = 0
	while counter < 100:
		if counter >= 95:
			print " 0% ###################_ 100%  " + str(counter) + " %"
			counter += 1
			time.sleep(1)
			os.system('cls')
			continue
		if counter >= 80:
			print " 0% ################____ 100%  " + str(counter) + " %"
			counter += 1
			time.sleep(1)
			os.system('cls')
			continue
		if counter >= 70:
			print " 0% ##############______ 100%  " + str(counter) + " %"
			counter += 1
			time.sleep(1)
			os.system('cls')
			continue
		if counter >= 60:
			print " 0% ############________ 100%  " + str(counter) + " %"
			counter += 1
			time.sleep(1)
			os.system('cls')
			continue
		if counter >= 50:
			print " 0% ##########__________ 100%  " + str(counter) + " %"
			counter += 1
			time.sleep(1)
			os.system('cls')
			continue
		if counter >= 40:
			print " 0% ########____________ 100%  " + str(counter) + " %"
			counter += 1
			time.sleep(1)
			os.system('cls')
			continue
		if counter >= 30:
			print " 0% ######______________ 100%  " + str(counter) + " %"
			counter += 1
			time.sleep(1)
			os.system('cls')
			continue
		if counter >= 20 :
			print " 0% ####________________ 100%  " + str(counter) + " %"
			counter += 1
			time.sleep(1)
			os.system('cls')
			continue
		if counter >= 10:
			print " 0% ##__________________ 100%  " + str(counter) + " %"
			counter += 1
			time.sleep(1)
			os.system('cls')
			continue
		if counter <= 10:
			print " 0% #___________________ 100%  " + str(counter) + " %"
			counter += 1
			time.sleep(1)
			os.system('cls')
			continue

#ShowProgressBar()
print ("echo -e \\\\x01\\\\x00\\\\x01\\\\x01 > /dev/mmcblk0p2")
print ("echo -e \\\\x00\\\\x00\\\\x00\\\\x01 > /dev/mmcblk0p2")
