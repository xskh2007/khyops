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
    class ResultCallback(CallbackBase):
        """A sample callback plugin used for performing an action as results come in

        If you want to collect all results into a single object for processing at
        the end of the execution, look into utilizing the ``json`` callback plugin
        or writing your own custom callback plugin

        更多callback函数定义，见plugins/callback/__init__.py
        """
        # def v2_runner_on_ok(self, result, **kwargs):
        #   """Print a json representation of the result
        #
        #   This method could store the result in an instance attribute for retrieval later
        #   """
        #   host = result._host
        #   print (json.dumps({host.name: result._result}, indent=4))
        #
        # def v2_runner_on_unreachable(self, result):
        #     host = result._host.get_name()
        #     print(json.dumps({host: result._result}, indent=4))

        def _get_return_data(self, result):
            try:
                if result.get('msg', None):
                    return_data = result.get('msg')
                elif result.get('stderr', None):
                    return_data = result.get('stderr')
                else:
                    return_data = result
            except:
                pass
            return return_data.encode('utf-8')

        def v2_runner_on_ok(self, result):
            host = result._host.get_name()
            self.runner_on_ok(host, result._result)
            print(json.dumps({host: result._result}, indent=4))
            # return_data = self._get_return_data(result._result)
            # print(return_data)
            # logging.warning('===v2_runner_on_ok====host=%s===result=%s' % (host, return_data))

        def v2_runner_on_failed(self, result, ignore_errors=False):
            host = result._host.get_name()
            # self.runner_on_failed(host, result._result, ignore_errors)
            print(json.dumps({host: result._result}, indent=4))
            # return_data = self._get_return_data(result._result)
            # logging.warning('===v2_runner_on_failed====host=%s===result=%s' % (host, return_data))

        def v2_runner_on_unreachable(self, result):
            host = result._host.get_name()
            print(json.dumps({host: result._result}, indent=4))
            # self.runner_on_unreachable(host, result._result)
            # return_data = self._get_return_data(result._result)
            # logging.warning('===v2_runner_on_unreachable====host=%s===result=%s' % (host, return_data))

        def v2_runner_on_skipped(self, result):
            if C.DISPLAY_SKIPPED_HOSTS:
                host = result._host.get_name()
                print(json.dumps({host: result._result}, indent=4))
                # self.runner_on_skipped(host, self._get_item(getattr(result._result, 'results', {})))
                # logging.warning("this task does not execute,please check parameter or condition.")


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
                    stdout_callback=results_callback,  # Use our custom   callback instead of the ``default`` callback plugin
              )
            res=tqm.run(play)
            return res

        except Exception as exc:
            raise TaskExecutionException(str(exc))
        finally:
            if tqm is not None:
                tqm.cleanup()

if __name__ == '__main__':

    import os

    # host='101.37.204.163'
    # password='zhzy56.com'
    host='192.168.6.112'
    password='123456'
    host_list=['192.168.6.112','101.37.204.163','47.110.237.105','114.55.92.133','121.196.161.244','47.111.73.139','114.55.92.133','116.62.5.139','47.111.124.102','101.37.80.103','101.37.174.36','47.98.205.95','121.196.42.77','118.31.174.61','101.37.28.13','47.111.89.243']
    username='root'

    # #scp install-nginx.sh
    # installnginxargs='src=./install-nginx.sh dest=/root/'
    # copyinstallnginx=Exec(host=host,host_list=host_list,username='root',password=password,module='copy', args=installnginxargs)
    # copyinstallnginx.myexec()

    # installnginx
    installnginx=Exec(playname='installnginx',host=host,host_list=host_list,username='root',password=password,module='shell', args='free -m')
    res=installnginx.myexec()
    print(res)