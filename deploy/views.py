from django.shortcuts import render
from deploy import models
from django.shortcuts import redirect
from django.http import JsonResponse,HttpResponse
from .ansibleapi import Exec
from .newansibleapi import Exec as NewExec
from .task import *
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required


# Create your views here.
from django.http import HttpResponse

@login_required
def index(request):
    assets = models.Servers.objects.all()
    # print(assets)
    return render(request, 'deploy/assets.html', locals())
    # return render(request, 'deploy/index.html', locals())


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html', locals())

    if request.method == 'POST':

        name = request.POST.get('name')
        password = request.POST.get('password')
        # 验证用户名和密码，验证通过的话，返回user对象
        user = auth.authenticate(username=name, password=password)
        print(name,password,user)
        if user:
            # 验证成功 登陆
            auth.login(request, user)
            print("登陆成功")
            return render(request, 'deploy/assets.html')

        else:
            print("登陆失败")
            return HttpResponseRedirect('/login')

def logout(request):
    if request.method == 'GET':
        auth.logout(request)
        return HttpResponseRedirect('/login')

@login_required
def addserver(request):
    if request.method == "POST":
        print(request.POST)
        company = request.POST["company"]
        domain = request.POST["domain"]
        serverip = request.POST["serverip"]
        password = request.POST["password"]
        deployversion=request.POST["deployversion"]
        pid=request.POST["pid"]
        iswww=request.POST.getlist("iswww")
        deploymodel=request.POST["deploymodel"]
        print(deploymodel,iswww)
        if request.POST["region"].strip()=="" or request.POST["region"]==None:
            region = "山西"
        else:
            region = request.POST["region"]
        icpurl = request.POST["icpurl"]

        # print username, password, email, address, cards, numbers
        if len(iswww) >0:
            models.Servers.objects.create(company=company, domain=domain, ip=serverip, password=password, region=region,
                                          icpurl=icpurl,
                                          deploymodel=deploymodel, deployversion=deployversion, pid=pid,iswww=1)
        elif len(iswww)==0:
            models.Servers.objects.create(company=company,domain=domain,ip=serverip,password=password,region=region,icpurl=icpurl,
                                      deploymodel=deploymodel,deployversion=deployversion,pid=pid,iswww=0)
        # models.User.objects.create(user_name=username, user_password=password, user_email=email, user_address=address,
                                   # user_cards=cards, user_numbers=numbers)
        return redirect('/deploy/')
    if request.method == "GET":
        assets = models.Servers.objects.all()
        print(assets)
        return render(request, 'deploy/addserver.html', locals())
        # return render(request, 'deploy/index.html', locals())

@login_required
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
    deployversion=models.Servers.objects.get(ip=host).deployversion
    pid=models.Servers.objects.get(ip=host).pid
    iswww=models.Servers.objects.get(ip=host).iswww
    icpurl=models.Servers.objects.get(ip=host).icpurl
    print('ppppppppppppppppppppp',deployversion)
    if deployversion==0:
        #老版本部署
        if region=="贵州":
            proxy_domain="56fanyun.com"
        else:
            proxy_domain = "kuaihuoyun.com"
        res=onekeydeploy.delay(host=host,domain=domain,password=password,company=company,proxy_domain=proxy_domain,deploymodel=deploymodel,icpurl=icpurl)
        # res=add.delay(3,5)
        print(res,"mmmmmmmmmmmmmmmmmmmm")
        return HttpResponse("网站部署中,请稍等片刻,刷新页面查看部署状态...")
    elif deployversion==1:
        #新版本部署
        print(deployversion,pid)
        res=newonekeydeploy.delay(host=host,domain=domain,password=password,company=company,deploymodel=deploymodel,icpurl=icpurl,pid=pid,iswww=iswww)
        print(res,"mmmmmmmmmmmmmmmmmmmm")
        return HttpResponse("网站部署中,请稍等片刻,刷新页面查看部署状态...")


@login_required
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

@login_required
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
