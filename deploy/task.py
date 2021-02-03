# -*- coding: utf-8 -*-
from celery import shared_task
import time
import sys
from .ansibleapi import Exec
import os
from deploy.models import Servers
import deploy
from multiprocessing import current_process
import subprocess
from deploy import models

deploypath = os.path.dirname(deploy.__file__)

@shared_task
def add(x, y):
    time.sleep(10)
    return x + y

@shared_task
def mul(x, y):
    time.sleep(10)
    return x * y

@shared_task
def xsum(numbers):
    time.sleep(10)
    return sum(numbers)

#host="",host_list,domain="",password="",company="",proxy_domain=""
@shared_task
def onekeydeploy(host="",domain="",password="",company="",proxy_domain="",deploymodel=""):
    # from multiprocessing import current_process
    # current_process()._config = {'semprefix': '/mp'}
    current_process()._config = {'semprefix': '/mp'}

    # host='192.168.6.40'
    # domain='zizwl.com'
    # password='123456'
    # company='贵州紫竹物联科技有限公司'
    # proxy_domain='56fanyun.com'
    task_res={}
    username='root'
    # host_list=['192.168.6.40']
    host_list=list(Servers.objects.values_list('ip', flat=True))
    br='master'
    icpurl='http://5ff2d1dd84d6b.icp.jinsan168.com/t/5ff2d1dd84d6b'
    # res=os.popen("sh "+deploypath+"/init.sh "+domain+" "+br+" "+proxy_domain+" "+company+" "+icpurl).readlines()

    #生成nginx配置文件，替换icpurl
    cmd="sh "+deploypath+"/init.sh "+domain+" "+br+" "+proxy_domain+" "+company+" "+icpurl
    cmd_res=subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    print(cmd_res[1],"res33333333333")
    if len(cmd_res[1])==0:
        task_res["cmd_res"]="success"
        print("success")
    else:
        task_res["cmd_res"] = "fail"
        print("fail")

    #拷贝nginx安装脚本
    installnginxargs="src="+deploypath+"/install-nginx.sh dest=/root/"
    copyinstallnginx=Exec(playname='copyinstallnginx',host=host,host_list=host_list,username=username,password=password,module='copy', args=installnginxargs)
    copyinstallnginx_res=copyinstallnginx.myexec()
    if copyinstallnginx_res==0:
        task_res["copyinstallnginx_res"] = "success"
    else:
        task_res["copyinstallnginx_res"] = "fail"
    print(copyinstallnginx_res)

    # 安装nginx
    installnginx=Exec(playname='installnginx',host=host,host_list=host_list,username=username,password=password,module='shell', args='sh /root/install-nginx.sh')
    installnginx_res=installnginx.myexec()
    if installnginx_res==0:
        task_res["installnginx_res"] = "success"
    else:
        task_res["installnginx_res"] = "fail"
    print(installnginx_res)

    #拷贝nginx配置文件
    configurenginxargs="src="+deploypath+"/temp/%s/nginx-wlhy.conf dest=/etc/nginx/sites-enabled/"%(domain)
    print("++++++++++++",domain,configurenginxargs,"-----------------")
    configurengin = Exec(playname='configurengin',host=host, host_list=host_list, username=username, password=password, module='copy', args=configurenginxargs)
    configurengin_res=configurengin.myexec()
    if configurengin_res==0:
        task_res["configurengin_res"] = "success"
    else:
        task_res["configurengin_res"] = "fail"
    print(configurengin_res)

    #拷贝acme
    acmeargs="src="+deploypath+"/pack/acme.sh.tar.gz dest=/root/"
    copyacme=Exec(playname='copyacme',host=host,host_list=host_list,username=username,password=password,module='copy', args=acmeargs)
    copyacme_res=copyacme.myexec()
    if copyacme_res==0:
        task_res["copyacme_res"] = "success"
    else:
        task_res["copyacme_res"] = "fail"
    print(copyacme_res)

    #拷贝acme脚本
    installacmeargs="src="+deploypath+"/pack/installacme.sh dest=/root/"
    copyacme=Exec(playname='copyacme',host=host,host_list=host_list,username=username,password=password,module='copy', args=installacmeargs)
    copyacme_res=copyacme.myexec()
    if copyacme_res==0:
        task_res["copyacme_res"] = "success"
    else:
        task_res["copyacme_res"] = "fail"
    print(copyacme_res)

    installacme=Exec(playname='installacme',host=host,host_list=host_list,username=username,password=password,module='shell', args='bash /root/installacme.sh %s'%(domain))
    installacme_res=installacme.myexec()
    if installacme_res==0:
        task_res["installacme_res"] = "success"
    else:
        task_res["installacme_res"] = "fail"
    print(installacme_res)

    if deploymodel==1:
        #拷贝index.html
        # scpindexxargs="src="+deploypath+"/temp/%s/ dest=/var/www/html/"%(domain)
        scpindexxargs="src=%s/temp/%s/ dest=/var/www/html/"%(deploypath,domain)
        scpindex = Exec(playname='scpindex',host=host, host_list=host_list, username=username, password=password, module='copy', args=scpindexxargs)
        scpindex_res=scpindex.myexec()
        if scpindex_res==0:
            task_res["scpindex_res"] = "success"
        else:
            task_res["scpindex_res"] = "fail"
        print("scpindex_res-------",scpindex_res)
    elif deploymodel==0:
        #拷贝整站
        scpindexxargs="src=%s/temp/celestia-customer-www.tar.gz  dest=/var/www/html/ mode=0755 copy=yes"%(deploypath)
        scpindex = Exec(playname='scpindex',host=host, host_list=host_list, username=username, password=password, module='unarchive', args=scpindexxargs)
        scpindex_res=scpindex.myexec()
        if scpindex_res==0:
            task_res["scpindex_res"] = "success"
        else:
            task_res["scpindex_res"] = "fail"
        print("scpindex_res-------",scpindex_res)

    for v in task_res.values():
        if v=="success":
            models.Servers.objects.filter(ip=host).update(deploystatus=1)
            print(v)
        elif v=="fail":
            models.Servers.objects.filter(ip=host).update(deploystatus=2)
            print(v)
            break
    return task_res