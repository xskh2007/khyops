#!/usr/bin/env python

import json
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase

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
results_callback = ResultCallback()
# ssh连接采用password认证
variable_manager.extra_vars={"ansible_user": "root", "ansible_ssh_pass": "123456"}
# 初始化inventory， host_list后面可以是列表或inventory文件
inventory = Inventory(loader=loader, variable_manager=variable_manager, host_list=['192.168.6.40'])
variable_manager.set_inventory(inventory)


# create play with tasks
play_source =  dict(
    name = "Ansible Play",
    hosts = 'all',   # 这里指定all
    gather_facts = 'no',
    tasks = [
        dict(action=dict(module='copy', args='src=/root/OpsManage-3.zip dest=/var/www/'), register='copy_out'),
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
    # result = tqm.run(play)
    # print(result)
    print(tqm)
    tqm.run(play)
finally:
    if tqm is not None:
        tqm.cleanup()