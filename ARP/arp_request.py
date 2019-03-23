# -*- coding=utf-8 -*-

import logging

logging.getLogger("kamene.runtime").setLevel(logging.ERROR)  # 清除报错
from kamene.all import *
from get_interface_ip import get_ip_address  # 获取本机IP地址
from get_interface_mac import get_mac_address  # 获取本机MAC地址
from kamene import kamene_iface  # 获取scapy iface的名字


def arp_request(ip_address, ifname='ens33'):
    # 获取本机IP地址
    localip = get_ip_address(ifname)
    # 获取本机MAC地址
    localmac = get_mac_address(ifname)
    try:  # 发送ARP请求并等待响应
        result_raw = sr1(ARP(op=1,
                             hwsrc=localmac,
                             hwdst='00:00:00:00:00:00',
                             psrc=localip,
                             pdst=ip_address),
                         iface=kamene_iface(ifname),
                         timeout=1,
                         verbose=False)
        return ip_address, result_raw.getlayer(ARP).fields['hwsrc']

    except AttributeError:
        return ip_address, None


if __name__ == '__main__':
    # Windows Linux均可使用
    # arp_result = arp_request('10.1.1.254', "Net1")
    arp_result = arp_request('10.1.1.254', "ens33")
    print("IP地址:", arp_result[0], "MAC地址:", arp_result[1])





