# -*- coding=utf-8 -*-

from netifaces import interfaces, ifaddresses, AF_INET, AF_INET6
import platform


def get_ip_address(ifname):
    if platform.system() == "Linux":
        return ifaddresses(ifname)[AF_INET][0]['addr']
    elif platform.system() == "Windows":
        from win_interface_name import win_from_name_get_id
        if_id = win_from_name_get_id(ifname)
        return ifaddresses(if_id)[AF_INET][0]['addr']
    else:
        print('操作系统不支持,本脚本只能工作在Windows或者Linux环境!')


def get_ipv6_address(ifname):
    if platform.system() == "Linux":
        return ifaddresses(ifname)[AF_INET6][0]['addr']
    elif platform.system() == "Windows":
        from win_interface_name import win_from_name_get_id
        if_id = win_from_name_get_id(ifname)
        return ifaddresses(if_id)[AF_INET6][0]['addr']
    else:
        print('操作系统不支持,本脚本只能工作在Windows或者Linux环境!')


if __name__ == "__main__":
    print(get_ip_address('VMware Network Adapter VMnet1'))
    # print(get_ipv6_address('VMware Network Adapter VMnet1'))
    # print(get_ip_address('ens33'))
    # print(get_ipv6_address('ens33'))

