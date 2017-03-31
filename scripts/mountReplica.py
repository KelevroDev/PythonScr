import os


def mountSharedDir(netPath, user, password, winDrive):
    print("Connecting to [%s]" % netPath)
    os.system('NET USE %s: %s /USER:"%s" "%s"' % (winDrive, netPath, user, password))


def unmountSharedDir(winDrive):
    print("Unmounting disk [%s]" % winDrive)
    os.system('NET USE %s: /delete' % (winDrive))



mountSharedDir("\\\\hirowsfsvs01.ad.harman.com\TOYOTA\Toyota_CY17_MEU",
               "ADHARMAN\SKalinina",
               "Harman/0588",
               "Z")

#unmountSharedDir("Z")
