import paramiko

host = "172.30.136.145"
user = "root"
password = "root"
port = 22

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(host, port, user, password)


stdin, stdout, stderr = client.exec_command("/usr/bin/InputManagerTester --tp=/usr/bin/Test.hbtc")
stdin.write("r\n")
stdin.flush()
stdin.write("q\n")
stdin.flush()
print(stdout.read().decode())

client.close()
