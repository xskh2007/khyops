#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import namedtuple
# 核心类
# 用于读取YAML和JSON格式的文件
import sys
from ansible.parsing.dataloader import DataLoader
# 用于存储各类变量信息
# from ansible.vars.manager import VariableManager
from ansible.vars import VariableManager

# 用于导入资产文件
# from ansible.inventory.manager import InventoryManager
from ansible.inventory import Inventory

# 存储执行hosts的角色信息
from ansible.playbook.play import Play
# ansible底层用到的任务队列
from ansible.executor.task_queue_manager import TaskQueueManager
# 状态回调，各种成功失败的状态
from ansible.plugins.callback import CallbackBase


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


def useMyCallbackBase():
    """
    这里通过调用ad-hoc来使用自定义callback
    :return:
    """
    dl = DataLoader()
    vm = VariableManager()
    # im = InventoryManager(loader=dl, sources=["hosts"])
    host_list=['47.98.146.54','101.37.204.163']
    Options = namedtuple("Options", [
        "connection", "remote_user", "ask_sudo_pass", "verbosity", "ack_pass",
        "module_path", "forks", "become", "become_method", "become_user", "check",
        "listhosts", "listtasks", "listtags", "syntax", "sudo_user", "sudo", "diff"
    ])
    options = Options(connection='smart', remote_user=None, ack_pass=None, sudo_user=None, forks=5, sudo=None,
                      ask_sudo_pass=False,
                      verbosity=5, module_path=None, become=None, become_method=None, become_user=None, check=False,
                      diff=False,
                      listhosts=None, listtasks=None, listtags=None, syntax=None)
    play_source = dict(name="Ansible Play",  # 任务名称
                       hosts="47.98.146.54",  # 目标主机，可以填写具体主机也可以是主机组名称
                       gather_facts="no",  # 是否收集配置信息

                       # tasks是具体执行的任务，列表形式，每个具体任务都是一个字典
                       tasks=[
                           dict(action=dict(module="shell", args="touch /tmp/bbb.txt", warn=False))
                       ])
    variable_manager.extra_vars = {"ansible_user": "root", "ansible_ssh_pass": "yc56.com"}
    inventory = Inventory(loader=loader, variable_manager=variable_manager, host_list=self.host_list)
    variable_manager.set_inventory(inventory)
    play = Play().load(play_source, variable_manager=vm, loader=dl)

    passwords = dict()  # 这个可以为空，因为在hosts文件中

    mycallback = MyCallbackBase()  # 实例化自定义callback

    tqm = TaskQueueManager(
        inventory=inventory,
        variable_manager=vm,
        loader=dl,
        options=options,
        passwords=passwords,
        stdout_callback=mycallback  # 配置使用自定义callback
    )
    tqm.run(play)
    # print(mycallback.host_ok.items())  # 它会返回2个东西，一个主机一个是执行结果对象
    # 定义数据结构
    result_raw = {"success": {}, "failed": {}, "unreachable": {}}
    # 如果成功那么  mycallback.host_ok.items() 才可以遍历，上面的任务肯定能成功所以我们就直接遍历这个
    for host, result in mycallback.host_ok.items():
        result_raw["success"][host] = result._result

    for host, result in mycallback.host_failed.items():
        result_raw["failed"][host] = result._result

    for host, result in mycallback.host_unreachable.items():
        result_raw["unreachable"][host] = result._result

    print(result_raw)







def main():
    useMyCallbackBase()

if __name__ == "__main__":
    try:
        main()
    finally:
        sys.exit()