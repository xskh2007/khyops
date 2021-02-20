from django.shortcuts import render
from deploy import models
from django.shortcuts import redirect
from django.http import JsonResponse,HttpResponse
from .ansibleapi import Exec
from .newansibleapi import Exec as NewExec
from .task import *


# Create your views here.
from django.http import HttpResponse

def index(request):
    assets = models.Servers.objects.all()
    # print(assets)
    return render(request, 'deploy/assets.html', locals())
    # return render(request, 'deploy/index.html', locals())

def addserver(request):
    if request.method == "POST":
        print(request.POST)
        company = request.POST["company"]
        domain = request.POST["domain"]
        serverip = request.POST["serverip"]
        password = request.POST["password"]
        deploymodel=request.POST["deploymodel"]
        print(deploymodel)
        if request.POST["region"].strip()=="" or request.POST["region"]==None:
            region = "山西"
        else:
            region = request.POST["region"]
        icpurl = request.POST["icpurl"]

        # print username, password, email, address, cards, numbers
        models.Servers.objects.create(company=company,domain=domain,ip=serverip,password=password,region=region,icpurl=icpurl,
                                      deploymodel=deploymodel)
        # models.User.objects.create(user_name=username, user_password=password, user_email=email, user_address=address,
                                   # user_cards=cards, user_numbers=numbers)
        return redirect('/deploy/')
    if request.method == "GET":
        assets = models.Servers.objects.all()
        print(assets)
        return render(request, 'deploy/addserver.html', locals())
        # return render(request, 'deploy/index.html', locals())


def deploy(request):
    # from multiprocessing import current_process
    # current_process()._config = {'semprefix': '/mp'}
    # ip = request.POST["ip"]
    # host_list=models.Servers.objects.values_list("ip", "47.111.73.139")
    #host_list=list(models.Servers.objects.values_list('ip', flat=True))
    host=request.POST["ip"]
    company=models.Servers.objects.get(ip=host).company
    domain=models.Servers.objects.get(ip=host).domain
    password=models.Servers.objects.get(ip=host).password
    region=models.Servers.objects.get(ip=host).region
    deploymodel=models.Servers.objects.get(ip=host).deploymodel
    icpurl=models.Servers.objects.get(ip=host).icpurl
    if region=="贵州":
        proxy_domain="56fanyun.com"
    else:
        proxy_domain = "kuaihuoyun.com"
    res=onekeydeploy.delay(host=host,domain=domain,password=password,company=company,proxy_domain=proxy_domain,deploymodel=deploymodel,icpurl=icpurl)
    # res=add.delay(3,5)
    print(res,"mmmmmmmmmmmmmmmmmmmm")
    return HttpResponse("网站部署中,请稍等片刻,刷新页面查看部署状态...")


def checkping(request):
    print(request.POST)
    host=request.POST["ip"]
    # password=models.Servers.objects.get(ip=host).password
    # domain=models.Servers.objects.get(ip=host).domain
    # host_list=list(models.Servers.objects.values_list('ip', flat=True))
    # host_list=list(models.Servers.objects.values_list('ip', flat=True))
    password=request.POST["password"]
    domain=request.POST["domain"]
    host_list=[host]
    print(host,host_list,password,domain)
    checkping = NewExec(playname='checkping', host=host, host_list=host_list, username='root', password=password,
                        module='shell', args='ping %s -c 3'%(domain))
    res = checkping.myexec()
    # print(res["stdout"])
    print(res)
    return HttpResponse(res["stdout"].replace("\n","<br>"))


def checkport443(request):
    host=request.POST["ip"]
    import socket;
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((host,443))
    if result == 0:
       return HttpResponse("443 is ok")
    else:
       return HttpResponse("443 is Not ok")


def checkport22(request):
    host=request.POST["ip"]
    import socket;
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((host,22))
    if result == 0:
       return HttpResponse("22 is ok")
    else:
       return HttpResponse("22 is Not ok")

def mytest(request):
    name_dict = {'twz': 'Love python and Django', 'zqxt': 'I am teaching Django'}
    return JsonResponse(name_dict)
