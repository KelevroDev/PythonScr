#!/usr/bin/env python


import datetime
import os
import check_sbcat
import paramiko


#class coord:
#	xor[x][y] = " "


def show():
	for i in range(20):
		if i==0:
			for j in range(23):
				print('-',end='')
		elif i == 19:
			for j in range(20):
				if j == 0:
					for j in range(23):
						print('_',end='')
		else:
			print('|',end='')
			for j in range(1,21):
				if j % 2 != 0:
					print (' ',end='')
				else:
					print('o',end='')
			print(' |',end='')
		print()


def ar():
	a = []
	b = []
	i = 0
	while i < 10:
		b.append("*")
		i = i + 1
	i = 0
	while i < 10:
		a.append(b)
		i = i + 1

	for t in a:
		print (t)





def main():
	ar()
	#cor = coord
	#show()





main()