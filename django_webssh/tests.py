from django.test import TestCase

# Create your tests here.
import paramiko

user="root"
password="Xhk12345"
host="121.41.195.10"
port="22"
timeout=60
term='xterm'
pty_width=80
pty_height=24


ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(username=user, password=password, hostname=host, port=port, timeout=timeout)
transport = ssh_client.get_transport()
channel = transport.open_session()
channel.get_pty(term=term, width=pty_width, height=pty_height)
channel.invoke_shell()


channel.send("date \n")
channel.send("\n")

for i in range(2):
    recv = channel.recv(1024).decode('utf-8')
    print(recv)

    # print(recv)
# print(channel)
#