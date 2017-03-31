#!/usr/bin/env python
# -*- coding: utf8 -*-
import sys
import os
import random
import time
import threading
import FolderCopy
import Upload_Configure
import datetime
import win32com.client as win32

def printInfo():
    print("""
        ###############################################
        #             Wellcome to Info                #
        #                                             #
        # ? - all commands     |                      #
        #                      |                      #
        # a - dounload new SW  |                      #
        #                      |                      #
        # q - work             |                      #
        #                      |                      #
        # e - Send an email    |                      #
        #                      |                      #
        # t - time             |                      #
        #                      |                      #
        # p - print            |  c - exit            #
        #                                             #       
        #██▓▓▓▒▒▒░░░     _  _^v^_  _       ░░░▒▒▒▓▓▓██#
        #██▓▓▓▒▒▒░░░      \_(*_*)_/        ░░░▒▒▒▓▓▓██#
        #██▓▓▓▒▒▒░░░                       ░░░▒▒▒▓▓▓██#
        ###############################################
        """)
    time()

def time():
    nowTime = str(datetime.datetime.now())
    print ("\n        ░░░▒▒▒▓▓▓██  ", nowTime[:19], "  ██▓▓▓▒▒▒░░░\n\n")

def SendEmail(name, text):
    print ("Sending e-mail")
    nowTime = str(datetime.datetime.now())
    emailText = "\nDate: " + nowTime[:19]
    MailHeader = "Hello,\nI need to say now " + emailText
    signature = "\n\n\nCreated by:\nE. Kiriyanov - The Best of the Best\nEKiriyanov@luxoft.com"
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    #mail.To = 'ekiriyanov@luxoft.com; skalinina@luxoft.com; dleu@luxoft.com'
    #mail.To = 'ekiriyanov@luxoft.com'
    mail.To = name
    mail.Subject = "All I need: e-mail"
    mail.body = MailHeader + "\n\n" + text + signature
    mail.send
    print ("E-mail sended" + str(nowTime))

def main_func(answer):
    x = answer
    if x == "?":
        printInfo()
    if x == "q":
        print ("OK")
        Upload_Configure.main()
    if x == "c":
        print ("EXIT")
    if x == "a":
    	FolderCopy.main()
    if x == "e":
        name = input("E-mail address: ")
        someText = input("What text should we send to " + name + "? ")
        SendEmail(name, someText)
        print ("Mail sent!!!")
    if x == "t":
        time()
    if x == 'p':
        printMy()


def printMy():
    text = input("Text : ")
    for i in text:
        print (i)


def timer():
    global countTime
    global block
    countTime = 0
    block = 0
    while block != 1:
        time.sleep(1)
        countTime = countTime + 1

def run_main():
    answer = "?"
    while answer != "c":
        main_func(answer)
        answer = input("What shold we do? ")
        
#dd if=meucy17_20170228T132846.emmc.img bs=4096 | gzip -c | split -b 2G - meucy17_20170228T132846.emmc.img.gz
run_main()