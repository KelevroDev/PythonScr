import hashlib

def hash_file(filename):
  h = hashlib.sha1()
  with open(filename,'rb') as file:
    chunk = 0
    while chunk != b'':
      chunk = file.read(1024)
      h.update(chunk)
  return h.hexdigest()

message = hash_file("E:\EMAGES\TOYOTA_CY17_MEU_A16011A_AppOnlDiagHMISWSysSWUpdVR_A+.ext3")
print(message)


def checkPartition():
  #x = SerialConnection("COM9", "115200")
  #x.open()
  x.run("mount")
  outPut = x.readOutput()
  print (outPut)
  if outPut.endswith('/dev/mmcblk0p6 on / type ext3'):
    part = 6
  if outPut.endswith('/dev/mmcblk0p8 on / type ext3'):
    part = 8
  #x.close()
  return part

def flashing():
  x = SerialConnection("COM9", "115200")
  x.open()
  x.run("root")
  time.sleep(1)
  x.run("root")
  time.sleep(1)
  x.run("mount /dev/sda1 /mnt")
  time.sleep(2)
  version = checkVersion()
  if fileName.endswith(version) == -1:
    part = checkPartition()
    if part == 8:
      x.run("dd if=/mnt/"+ fileName + " of=/dev/mmcblk0p6")
      x.run("echo -e \\x01\\x00\\x01\\x01 > /dev/mmcblk0p2")
      x.run("sync")
    if part == 6:
      x.run("dd if=/mnt/"+ fileName + " of=/dev/mmcblk0p8")
      x.run("echo -e \\x00\\x00\\x00\\x01 > /dev/mmcblk0p2")
      x.run("sync")
    else:
      print ("ERROR - pertitions issue!!!")

  x.run("reboot -f")
  time.sleep(30)
  x.readOutput()
  x.run("root")
  time.sleep(1)
  x.run("root")
  x.readOutput()
  time.sleep(1)
  x.run("udhcpc -i eth0")
  time.sleep(10)
  ver = checkVersion()
  print (ver)
  x.close()
  #x.run("version")
  #x.run("reboot -f")
  #time.sleep(2)
  #x.run("c")
  #time.sleep(1)
  #x.run("mmc dev2")
  #time.sleep(2)
  #x.run("mmc read 0x10800000 800 5000")
  #time.sleep(2)
  #x.run("bootm")
  #time.sleep(15)
  #x.run("mount /dev/sda1 /mnt")
  #time.sleep(1)
  #x.run("dd if=/mnt/" + fileName + " of=/dev/mmcblk0p6")
  #x.run("dd if=/mnt/" + fileName + " of=/dev/mmcblk0p6")
  #time.sleep(700)
  #x.run("reboot -f")
  #time.sleep(60)
  #x.run("udhcpc -i eth0")
  #time.sleep(5)
  #x.run("version")
  #x.close()

#changing to partition 6: echo -e \\x01\\x00\\x01\\x01 > /dev/mmcblk0p2
 
#changing to partition 8: echo -e \\x00\\x00\\x00\\x01 > /dev/mmcblk0p2
