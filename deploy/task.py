
from celery import shared_task
import time
import sys
from .ansibleapi import Exec
import os
from deploy.models import Servers
import deploy
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
    print("sh "+deploypath+"./init.sh "+domain+br+proxy_domain+company+icpurl)
    res=os.popen("sh "+deploypath+"/init.sh "+domain+" "+br+" "+proxy_domain+" "+company+" "+icpurl).readlines()


    #scp install-nginx.sh
    installnginxargs="src="+deploypath+"./install-nginx.sh dest=/root/"
    copyinstallnginx=Exec(host=host,host_list=host_list,username=username,password=password,module='copy', args=installnginxargs)
    copyinstallnginx.myexec()

    # installnginx
    installnginx=Exec(host=host,host_list=host_list,username=username,password=password,module='shell', args='sh /root/install-nginx.sh')
    installnginx.myexec()

    configurenginxargs="src="+deploypath+"/temp/%s/nginx-wlhy.conf dest=/etc/nginx/sites-enabled/"%(domain)
    print(domain,configurenginxargs,"-----------------")
    configurengin = Exec(host=host, host_list=host_list, username=username, password=password, module='copy', args=configurenginxargs)
    configurengin.myexec()

    acmeargs="src="+deploypath+"/pack/acme.sh.tar.gz dest=/root/"
    copyacme=Exec(host=host,host_list=host_list,username=username,password=password,module='copy', args=acmeargs)
    copyacme.myexec()

    installacmeargs="src="+deploypath+"/pack/installacme.sh dest=/root/"
    copyacme=Exec(host=host,host_list=host_list,username=username,password=password,module='copy', args=installacmeargs)
    copyacme.myexec()

    installacme=Exec(host=host,host_list=host_list,username=username,password=password,module='shell', args='bash /root/installacme.sh %s'%(domain))
    installacme.myexec()

    #scp index.html
    print ("wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww")
    scpindexxargs="src="+deploypath+"/temp/%s/ dest=/var/www/html/"%(domain)
    print(scpindexxargs,"-----------------")
    scpindex = Exec(host=host, host_list=host_list, username=username, password=password, module='copy', args=scpindexxargs)
    scpindex.myexec()

    return "ok"