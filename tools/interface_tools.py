# -*- coding=utf-8 -*-

import logging
logging.getLogger("kamene.runtime").setLevel(logging.ERROR)  # 清除报错
from kamene.all import *
import platform


def kamene_iface(os_name):
    if platform.system() == "Linux":
        return os_name
    elif platform.system() == "Windows":
        for x, y in ifaces.items():
            # print(x, y)
            if y.pcap_name is not None:
                # print(y.pcap_name)
                if get_ifname(os_name) == ('{' + y.pcap_name.split('{')[1]):
                    return x
                else:
                    pass


def get_ifname(ifname):
    if platform.system() == "Linux":
        return ifname
    elif platform.system() == "Windows":
        return win_from_name_get_id(ifname)
    else:
        return None


def get_connection_name_from_guid(iface_guids):
    import winreg as wr
    # 产生接口名字清单,默认全部填写上'(unknown)'
    iface_dict = {}
    # 打开"HKEY_LOCAL_MACHINE"
    reg = wr.ConnectRegistry(None, wr.HKEY_LOCAL_MACHINE)
    # 打开r'SYSTEM\CurrentControlSet\Control\Network\{4d36e972-e325-11ce-bfc1-08002be10318}'
    #
    reg_key = wr.OpenKey(reg, r'SYSTEM\CurrentControlSet\Control\Network\{4d36e972-e325-11ce-bfc1-08002be10318}')
    for i in range(len(iface_guids)):
        try:
            # 尝试读取每一个接口ID下对应的Name
            # print(iface_guids[i])
            reg_subkey = wr.OpenKey(reg_key, iface_guids[i] + r'\Connection')
            # 如果存在Name,写入iface_dict字典
            iface_dict[wr.QueryValueEx(reg_subkey, 'Name')[0]] = iface_guids[i]
        except FileNotFoundError:
            pass
    # 返回iface_dict
    return iface_dict


def win_from_name_get_id(ifname):
    import netifaces as ni
    x = ni.interfaces()
    # print(x)
    return get_connection_name_from_guid(x).get(ifname)


from netifaces import interfaces, ifaddresses, AF_INET, AF_INET6


def get_ip_address(ifname):
    if platform.system() == "Linux":
        return ifaddresses(ifname)[AF_INET][0]['addr']
    elif platform.system() == "Windows":
        if_id = win_from_name_get_id(ifname)
        return ifaddresses(if_id)[AF_INET][0]['addr']
    else:
        print('操作系统不支持,本脚本只能工作在Windows或者Linux环境!')


def get_ipv6_address(ifname):
    if platform.system() == "Linux":
        return ifaddresses(ifname)[AF_INET6][0]['addr']
    elif platform.system() == "Windows":
        if_id = win_from_name_get_id(ifname)
        return ifaddresses(if_id)[AF_INET6][0]['addr']
    else:
        print('操作系统不支持,本脚本只能工作在Windows或者Linux环境!')


if __name__ == "__main__":
    # print(get_ip_address('VMware Network Adapter VMnet1'))
    # print(get_ipv6_address('VMware Network Adapter VMnet1'))
    # print(get_ip_address('ens33'))
    # print(get_ipv6_address('ens33'))

    # print(win_from_name_get_id("VMware Network Adapter VMnet1"))

    # print(get_ifname("VMware Network Adapter VMnet1"))

    print(kamene_iface('ens33'))

