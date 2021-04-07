from django.shortcuts import render

# Create your views here.

def sshindex(request):
    return render(request, 'mywebssh/index.html')



from django.shortcuts import render,HttpResponse
import subprocess,json

def myterm(request):
    if request.method == "POST":
        data = request.body.decode("utf-8")
        if data == "ok":
            proc = subprocess.Popen("ifconfig",stdout=subprocess.PIPE,shell=True)
            cc = str(proc.stdout.readlines())
            return HttpResponse(json.dumps({"cmd":cc}))
    return render(request, "mywebssh/index.html")



###########################

from django.shortcuts import render,HttpResponse
import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

def ssh_cmd(user,passwd,port,cmd):
    ssh.connect("192.168.6.111",port=port,username=user,password=passwd)
    cmd=cmd
    stdin, stdout, stderr = ssh.exec_command(cmd)
    result = stdout.read()
    if not result:
        result=stderr.read()
    ssh.close()
    return result.decode()

def myterm2(request):
    if request.method == "POST":
        data = request.body.decode("utf-8")
        if data == "ok":
            a = ssh_cmd("root","123456","22","ifconfig")
            return HttpResponse(a)
    return render(request, "mywebssh/index2.html")

###################################

from django.shortcuts import render,HttpResponse
import paramiko,json,time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

def ssh_shell(address,username,password,port,command):
    try:
        ssh.connect(address,port=port,username=username,password=password)
        stdin, stdout, stderr = ssh.exec_command(command)
        result = stdout.read()
        if not result:
            result=stderr.read()
        ssh.close()
        return result.decode()
    except Exception:
        ssh.close()
def myterm3(request):
    if request.method == "POST":
        data = request.body.decode("utf-8")
        json_data = json.loads(data)
        address = json_data.get("address")
        command = json_data.get("command")
        if len(address) >=2 and len(command) >=2:
            ret = ssh_shell(address,"root","123456","22",command)
            if ret !=None:
                times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                times = "---> \x1B[1;3;32m 执行时间: [ {} ] \x1B[0m".format(times)
                address = "\x1B[1;3;33m 主机地址: [ {} ] \x1B[0m".format(address)
                command = "\x1B[1;3;35m 执行命令: [ {} ] \x1B[0m".format(command)
                retn = times + address + command + "\x1B[1;3;25m 回执: [ok] \x1B[0m"
                return HttpResponse(retn)
            else:
                times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                times = "---> \x1B[1;3;32m 执行时间: [ {} ] \x1B[0m".format(times)
                address = "\x1B[1;3;33m 主机地址: [ {} ] \x1B[0m".format(address)
                command = "\x1B[1;3;35m 执行命令: [ {} ] \x1B[0m".format(command)
                retn = times + address + command + "\x1B[1;3;20m 回执: [Error] \x1B[0m"
                return HttpResponse(retn)
        else:
            return HttpResponse("主机地址或命令行不能为空...")
    return render(request, "mywebssh/index3.html")



#################echo
from django.shortcuts import render,HttpResponse
from dwebsocket.decorators import accept_websocket,require_websocket

def mywebsocket(request):
    return render(request,"mywebssh/websocket.html")

@accept_websocket
def echo(request):
    if not request.is_websocket():#判断是不是websocket连接
        print("不是websocket连接")
        try:#如果是普通的http方法
            message = request.GET['message']
            return HttpResponse(message)
        except:
            return render(request,'mywebssh/websocket.html')
    else:
        print("这是websocket连接")
        for message in request.websocket:
            request.websocket.send(message)#发送消息到客户端