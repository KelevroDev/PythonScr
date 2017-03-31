import psutil

PROCNAME = "calc.exe"
procFind = 0
for proc in psutil.process_iter():
    if proc.name() == PROCNAME :
    	proc.kill()
        procFind = 1
        print ("calc - killed")
if procFind == 0:
    print ("No process CALC running")