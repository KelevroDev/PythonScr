#!/usr/bin/env python
# -*- coding: utf8 -*-
import sys
import os
import random
import time
import numpy as np
import math
import yaml
import urllib
from os import listdir
from os.path import isfile
from P4 import P4,P4Exception
#import copy
from os.path import join as joinpath
global twf
global wtf

class calculator:
	def sum(self, x, y):
		res = x + y
		print x, "+", y, "=", res 
	def minus(self, x, y):
		res = x - y
		print x, "-", y, "=", res 
	def multiply(self, x, y):
		res = x * y
		print x, "*", y, "=", res
	def divided(self, x, y):
		res = x / y
		print x, "/", y, "=", res

def main():
	calc = calculator()
	action = 'a'
	while action != 'c':
		action = raw_input("Action > ")
		if action == 'c':
			return
		x = raw_input("X > ")
		if x 
		y = raw_input("Y > ")
		if action == '+':
			calc.sum(int(x), int(y)) 
		if action == '-':
			calc.minus(int(x), int(y))
		if action == '/':
			calc.divided(int(x), int(y))
		if action == '*':
			calc.multiply(int(x), int(y))
		else:
			print "* - multiply, + - summ, - - minus, / - divided,"

if __name__ == "__main__":
	main()