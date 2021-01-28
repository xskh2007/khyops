
from celery import shared_task
import time
import sys
from .ansibleapi import Exec
import os
from deploy.models import Servers
import deploy
from multiprocessing import current_process

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
def onekeydeploy(host="",domain="",password="",company="",proxy_domain=""):
    # from multiprocessing import current_process
    # current_process()._config = {'semprefix': '/mp'}
    current_process()._config = {'semprefix': '/mp'}

    # host='192.168.6.40'
    # domain='zizwl.com'
    # password='123456'
    # company='贵州紫竹物联科技有限公司'
    # proxy_domain='56fanyun.com'

    username='root'
    # host_list=['192.168.6.40']
    host_list=list(Servers.objects.values_list('ip', flat=True))
    br='master'
    icpurl='http://5ff2d1dd84d6b.icp.jinsan168.com/t/5ff2d1dd84d6b'
    print("sh "+deploypath+"/init.sh "+domain+br+proxy_domain+company+icpurl)
    res=os.popen("sh "+deploypath+"/init.sh "+domain+" "+br+" "+proxy_domain+" "+company+" "+icpurl).readlines()
    print(res,"resresresres333")

    #scp install-nginx.sh
    installnginxargs="src="+deploypath+"/install-nginx.sh dest=/root/"
    copyinstallnginx=Exec(playname='copyinstallnginx',host=host,host_list=host_list,username=username,password=password,module='copy', args=installnginxargs)
    copyinstallnginx_res=copyinstallnginx.myexec()
    print(copyinstallnginx_res)

    # installnginx
    installnginx=Exec(playname='installnginx',host=host,host_list=host_list,username=username,password=password,module='shell', args='sh /root/install-nginx.sh')
    installnginx_res=installnginx.myexec()
    print(installnginx_res)

    configurenginxargs="src="+deploypath+"/temp/%s/nginx-wlhy.conf dest=/etc/nginx/sites-enabled/"%(domain)
    print("++++++++++++",domain,configurenginxargs,"-----------------")
    configurengin = Exec(playname='configurengin',host=host, host_list=host_list, username=username, password=password, module='copy', args=configurenginxargs)
    configurengin_res=configurengin.myexec()
    print(configurengin_res)

    acmeargs="src="+deploypath+"/pack/acme.sh.tar.gz dest=/root/"
    copyacme=Exec(playname='copyacme',host=host,host_list=host_list,username=username,password=password,module='copy', args=acmeargs)
    copyacme_res=copyacme.myexec()
    print(copyacme_res)

    installacmeargs="src="+deploypath+"/pack/installacme.sh dest=/root/"
    copyacme=Exec(playname='copyacme',host=host,host_list=host_list,username=username,password=password,module='copy', args=installacmeargs)
    copyacme_res=copyacme.myexec()
    print(copyacme_res)

    installacme=Exec(playname='installacme',host=host,host_list=host_list,username=username,password=password,module='shell', args='bash /root/installacme.sh %s'%(domain))
    installacme_res=installacme.myexec()
    print(installacme_res)


    #scp index.html
    scpindexxargs="src="+deploypath+"/temp/%s/ dest=/var/www/html/"%(domain)
    scpindex = Exec(playname='scpindex',host=host, host_list=host_list, username=username, password=password, module='copy', args=scpindexxargs)
    scpindex_res=scpindex.myexec()
    print(scpindex_res)

    return "ok"