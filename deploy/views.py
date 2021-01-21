from django.shortcuts import render
from deploy import models
from django.shortcuts import redirect
from django.http import JsonResponse,HttpResponse
from .ansibleapi import Exec
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
        if request.POST["region"].strip()=="" or request.POST["region"]==None:
            region = "山西"
        else:
            region = request.POST["region"]

        # print username, password, email, address, cards, numbers
        models.Servers.objects.create(company=company,domain=domain,ip=serverip,password=password,region=region)
        # models.User.objects.create(user_name=username, user_password=password, user_email=email, user_address=address,
                                   # user_cards=cards, user_numbers=numbers)
        return redirect('/deploy/')
    if request.method == "GET":
        assets = models.Servers.objects.all()
        print(assets)
        return render(request, 'deploy/addserver.html', locals())
        # return render(request, 'deploy/index.html', locals())


def deploy(request):
    # ip = request.POST["ip"]
    # host_list=models.Servers.objects.values_list("ip", "47.111.73.139")
    #host_list=list(models.Servers.objects.values_list('ip', flat=True))
    host=request.POST["ip"]
    company=models.Servers.objects.get(ip=host).company
    domain=models.Servers.objects.get(ip=host).domain
    password=models.Servers.objects.get(ip=host).password
    region=models.Servers.objects.get(ip=host).region
    if region=="贵州":
        proxy_domain="56fanyun.com"
    else:
        proxy_domain = "kuaihuoyun.com"
    res=onekeydeploy.delay(host=host,domain=domain,password=password,company=company,proxy_domain=proxy_domain)
    # res=add.delay(3,5)
    print(res,"mmmmmmmmmmmmmmmmmmmm")
    return HttpResponse("网站部署中,请稍等片刻查看部署状态...")


def mytest(request):
    name_dict = {'twz': 'Love python and Django', 'zqxt': 'I am teaching Django'}
    return JsonResponse(name_dict)
