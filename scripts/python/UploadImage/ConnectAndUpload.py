import os
from shutil import copyfile
import os, fnmatch, re

masks = ["*.ext3"]

destMy = "C:\\"
destUSB = "/mnt/"

dddathListD = os.walk("Z:\\Daily")
wwwathListD = os.walk("Z:\\Weekly")

print ("Upload")

