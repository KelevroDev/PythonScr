#!/usr/bin/env python
# -*- coding: utf8 -*-
import sys
import os
import random
import time
import threading

def progress():
    count = 0
    co = 1
    while count <= 100:
        if count % 5 == 0:
            sys.stdout.write("#" * co +"\ruploaded " + str(count) +" % ")
            co = co + 1
        x = random.uniform(0.1, 0.5)
        count = count + 1
        time.sleep(x)

def progressbar():
    b = random.randrange(10)
    d = random.randrange(10000)
    a = random.uniform(1, 10) 
    os.system("cls")
    print (str(a) + ">>upload </Title></t> {DCU %s MEU AAA-> SW A163xx*\nJob- %s/}" % (b, d))
    time.sleep(0.2)
    print ("loadload </Title></t> {AlluploadedFiles _ToPathInTargetA%sxx*\nJob - %s/}" % (b, b))
    time.sleep(0.2)
    print ("domain - </> -># //" + str(d + 46) + " + </App" + str(b) + " > " + str((d * b) + d) + "  ApplicationInterface - " + str(b + 7 * 2) + "#</Title 0" + str(b) + ">\r")
    sys.stdout.write(str(a) + ">> UPLOAD </Title></t> {DCU %s MEU AAA-> SW A163xx(+1)*Job- %s/}" % (b, d))
    time.sleep(1)
    sys.stdout.write("\nloadload </Title></t> {AlluploadedFiles _ToPathInTargetA%sxx*\n Task- %s/}" % (b, b))
    time.sleep(0.2)
    print ("\ndomain        " + str(a))
    time.sleep(0.2)
    print ("\ninterface 	" + str(a * 2))
    time.sleep(0.2)
    print ("ConnTC." + str(a + 3) + "12." + str(a + 7) + "3.11")
    time.sleep(0.2)
    print ("\n</mainLoad>" + str(d) + "</.SwS>\n </done>\n </prev.STR.OS ->" + str(d) + " />")
    time.sleep(0.2)
    print ("domain 		" + str(a))
    print ("APP </main> " + str(d * 3) + " </main>\n </start.main.load.OS+1#>\n </prev.STR+1+" + str(a * 3) + "># \n")
    print ("DOsC<17" + str(a) + "> _CoP+1 @" + str(a) + "\n QAnext>>" + str(a + 7) + "\n")
    progress()

def timer():
    global countTime
    global block
    countTime = 0
    block = 0
    while block != 1:
        time.sleep(1)
        countTime = countTime + 1
    #print ("FIISH - ", str(countTime))

def main():
    counter = input("Jobs should be done: ")
    num = counter
    t = threading.Thread(target=timer)
    t.daemon = True
    t.start()
    #counter = 50
    while int(counter) > 0:
        os.system('cls')
        progressbar()
        counter = int(counter) - 1
        print ("\n\nJobs left - " + str(counter))
        time.sleep(1)
    block = 1
    print ("Minutes left:", int(countTime / 60))
    print ("!!!Jobs done:", num)

if __name__ == '__main__':
    main()
