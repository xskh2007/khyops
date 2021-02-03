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
import logging



class Exec():
    def __init__(self,playname='',host='',host_list='',username='root',password='',**kwargs):
        self.playname=playname
        self.host = host
        self.host_list=host_list
        self.username = username
        self.password = password
        self.action = dict(kwargs)

    class MyCallbackBase(CallbackBase):
        """
        通过api调用ac-hoc的时候输出结果很多时候不是很明确或者说不是我们想要的结果，主要它还是输出到STDOUT，而且通常我们是在工程里面执行
        这时候就需要后台的结果前端可以解析，正常的API调用输出前端很难解析。 对比之前的执行 adhoc()查看区别。
        为了实现这个目的就需要重写CallbackBase类，需要重写下面三个方法
        """

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)  # python3中重载父类构造方法的方式，在Python2中写法会有区别。
            self.host_ok = {}
            self.host_unreachable = {}
            self.host_failed = {}

        def v2_runner_on_unreachable(self, result):
            """
            重写 unreachable 状态
            :param result:  这是父类里面一个对象，这个对象可以获取执行任务信息
            """
            self.host_unreachable[result._host.get_name()] = result

        def v2_runner_on_ok(self, result, *args, **kwargs):
            """
            重写 ok 状态
            :param result:
            """
            self.host_ok[result._host.get_name()] = result

        def v2_runner_on_failed(self, result, *args, **kwargs):
            """
            重写 failed 状态
            :param result:
            """
            self.host_failed[result._host.get_name()] = result

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
        mycallback = self.MyCallbackBase()
        # ssh连接采用password认证
        variable_manager.extra_vars={"ansible_user": self.username, "ansible_ssh_pass": self.password}
        # 初始化inventory， host_list后面可以是列表或inventory文件
        inventory = Inventory(loader=loader, variable_manager=variable_manager, host_list=self.host_list)
        variable_manager.set_inventory(inventory)
        C.HOST_KEY_CHECKING=False


        # create play with tasks
        play_source =  dict(
            name = self.playname,
            hosts = self.host,   # 这里指定all
            gather_facts = 'no',
            tasks = [
                dict(action=self.action, register='copy_out'),
                # dict(action=dict(module='debug', args=dict(msg='')))
                ]
          )
        play = Play().load(play_source, variable_manager=variable_manager, loader=loader)
        print(play)

        # actually run it
        tqm = None
        try:
            tqm = TaskQueueManager(
                    inventory=inventory,
                    variable_manager=variable_manager,
                    loader=loader,
                    options=options,
                    passwords=passwords,
                    stdout_callback=mycallback,  # Use our custom   callback instead of the ``default`` callback plugin
              )
            res=tqm.run(play)
            # print(mycallback.host_ok.items())
            result_raw = {"success": {}, "failed": {}, "unreachable": {}}
            # 如果成功那么  mycallback.host_ok.items() 才可以遍历，上面的任务肯定能成功所以我们就直接遍历这个
            for host, result in mycallback.host_ok.items():
                result_raw["success"][host] = result._result
                return result_raw["success"][host]

            for host, result in mycallback.host_failed.items():
                result_raw["failed"][host] = result._result
                return result_raw["failed"][host]

            for host, result in mycallback.host_unreachable.items():
                result_raw["unreachable"][host] = result._result
                return result_raw["unreachable"][host]

            # print(result_raw)
            # return result_raw

        except Exception as exc:
            raise TaskExecutionException(str(exc))
        finally:
            if tqm is not None:
                tqm.cleanup()

if __name__ == '__main__':

    import os

    # host='101.37.204.163'
    # password='zhzy56.com'
    host='120.27.251.58'
    password='tc56.com'
    host_list=['120.27.251.58']
    username='root'

    # #scp install-nginx.sh
    # installnginxargs='src=./install-nginx.sh dest=/root/'
    # copyinstallnginx=Exec(host=host,host_list=host_list,username='root',password=password,module='copy', args=installnginxargs)
    # copyinstallnginx.myexec()

    # installnginx
    # installnginx=Exec(playname='installnginx',host=host,host_list=host_list,username='root',password=password,module='shell', args='free -m')
    # res=installnginx.myexec()
    # print(res)

    test = Exec(playname='test', host=host, host_list=host_list, username='root', password=password,
                        module='shell', args='ping www.baidu.com -c 3')
    res = test.myexec()
    print(res["stdout"])
