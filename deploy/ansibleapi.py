#!/usr/bin/env python

import json
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase
from ansible import constants as C



class Exec():
    def __init__(self,host='',host_list='',username='root',password='',**kwargs):
        self.host = host
        self.host_list=host_list
        self.username = username
        self.password = password
        self.action = dict(kwargs)
    class ResultCallback(CallbackBase):
        """A sample callback plugin used for performing an action as results come in

        If you want to collect all results into a single object for processing at
        the end of the execution, look into utilizing the ``json`` callback plugin
        or writing your own custom callback plugin

        更多callback函数定义，见plugins/callback/__init__.py
        """
        def v2_runner_on_ok(self, result, **kwargs):
          """Print a json representation of the result

          This method could store the result in an instance attribute for retrieval later
          """
          host = result._host
          print (json.dumps({host.name: result._result}, indent=4))

    def myexec(self):
        # 设置需要初始化的ansible配置参数
        Options = namedtuple('Options', ['connection', 'module_path', 'forks', 'become', 'become_method', 'become_user', 'check'])
        # 初始化需要的对象
        variable_manager = VariableManager()
        loader = DataLoader()
        # connection这里用ssh连接方式，本地可以用local; module_path指定正确的ansible module路径
        options = Options(connection='smart', module_path=None, forks=100, become=None, become_method=None, become_user=None, check=False)
        # passwords = dict(vault_pass='secret')
        passwords = None

        # Instantiate our ResultCallback for handling results as they come in
        results_callback = self.ResultCallback()
        # ssh连接采用password认证
        variable_manager.extra_vars={"ansible_user": self.username, "ansible_ssh_pass": self.password}
        # 初始化inventory， host_list后面可以是列表或inventory文件
        inventory = Inventory(loader=loader, variable_manager=variable_manager, host_list=self.host_list)
        variable_manager.set_inventory(inventory)
        C.HOST_KEY_CHECKING=False


        # create play with tasks
        play_source =  dict(
            name = "Ansible Play",
            hosts = self.host,   # 这里指定all
            gather_facts = 'no',
            tasks = [
                dict(action=self.action, register='copy_out'),
                # dict(action=dict(module='debug', args=dict(msg='')))
                ]
          )
        play = Play().load(play_source, variable_manager=variable_manager, loader=loader)
        # print(play,"1111111111111111111")

        # actually run it
        tqm = None
        try:
            tqm = TaskQueueManager(
                    inventory=inventory,
                    variable_manager=variable_manager,
                    loader=loader,
                    options=options,
                    passwords=passwords,
                    stdout_callback=results_callback,  # Use our custom   callback instead of the ``default`` callback plugin
              )
            result = tqm.run(play)
            print(result,"2222222222222222")
            # print(tqm,"3333333333333333")
            # tqm.run(play)
            # print("444444444444")
        except Exception as exc:
            raise TaskExecutionException(str(exc))
        finally:
            if tqm is not None:
                tqm.cleanup()

if __name__ == '__main__':

    import os

    host='114.55.95.218'
    domain='zizwl.com'
    password='Cz@#3143'
    company='贵州紫竹物联科技有限公司'

    br='master'
    proxy_domain='56fanyun.com'
    icpurl='http://5ff2d1dd84d6b.icp.jinsan168.com/t/5ff2d1dd84d6b'
    print("sh ./init.sh "+domain+br+proxy_domain+company+icpurl)
    res=os.popen("sh ./init.sh "+domain+" "+br+" "+proxy_domain+" "+company+" "+icpurl).readlines()

    host_list=['114.55.95.218','47.110.237.105','114.55.92.133','121.196.161.244','47.111.73.139','114.55.92.133','116.62.5.139','47.111.124.102','101.37.80.103','101.37.174.36','47.98.205.95','121.196.42.77','118.31.174.61','101.37.28.13','47.111.89.243']
    username='root'
    args="src=./temp/%s dest=/var/www/"%(domain)
    print(args,"ggggggggggggggggggggggggggggggg")
    #dict(module='copy', args='src=/root/OpsManage-3.zip dest=/var/www/')

    #scp install-nginx.sh
    installnginxargs='src=./install-nginx.sh dest=/root/'
    copyinstallnginx=Exec(host=host,host_list=host_list,username='root',password=password,module='copy', args=installnginxargs)
    copyinstallnginx.myexec()

    # installnginx
    installnginx=Exec(host=host,host_list=host_list,username='root',password=password,module='shell', args='sh /root/install-nginx.sh')
    installnginx.myexec()

    configurenginxargs='src=./temp/%s/nginx-wlhy.conf dest=/etc/nginx/sites-enabled/'%(domain)
    print(domain,configurenginxargs,"-----------------")
    configurengin = Exec(host=host, host_list=host_list, username='root', password=password, module='copy', args=configurenginxargs)
    configurengin.myexec()

    acmeargs='src=./pack/acme.sh.tar.gz dest=/root/'
    copyacme=Exec(host=host,host_list=host_list,username='root',password=password,module='copy', args=acmeargs)
    copyacme.myexec()

    installacmeargs='src=./pack/installacme.sh dest=/root/'
    copyacme=Exec(host=host,host_list=host_list,username='root',password=password,module='copy', args=installacmeargs)
    copyacme.myexec()

    installacme=Exec(host=host,host_list=host_list,username='root',password=password,module='shell', args='bash /root/installacme.sh %s'%(domain))
    installacme.myexec()

    #scp index.html
    print ("wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww")
    scpindexxargs='src=./temp/%s/ dest=/var/www/html/'%(domain)
    print(scpindexxargs,"-----------------")
    scpindex = Exec(host=host, host_list=host_list, username='root', password=password, module='copy', args=scpindexxargs)
    scpindex.myexec()
