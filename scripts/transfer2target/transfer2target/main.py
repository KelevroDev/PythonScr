import paramiko
from Scp import SCPClient


targetIp = "172.30.136.145"
targetPort = "22"
targetUser = "root"
targetPassword = "root"

paramikoClient = paramiko.SSHClient()
paramikoClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
paramikoClient.connect(targetIp, int(targetPort), targetUser, targetPassword)

scpClient = SCPClient(paramikoClient.get_transport())

scpClient.put("text.txt", "/usr/")          # copy from pc to target
#scpClient.get("/usr/text2.txt", "D:\\")    # copy from target to pc



scpClient.close()
paramikoClient.close()