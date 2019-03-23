# -*- coding=utf-8 -*-

import platform
from kamene.all import *
import time
from get_interface_mac import get_mac_address


def arp_reply(dstip, ifname):
    # win_interfacename = 'VMware Network Adapter VMnet1'
    # cent_interfacename = 'ens33'
    for a in range(1, 10):
        if platform.system() == 'Linux':
            mac = get_mac_address(ifname)
            # 得到网卡mac
            pkt = Ether(src=mac, dst='ff:ff:ff:ff:ff:ff') / ARP(op=2, hwsrc=mac,
                                                                hwdst='ff:ff:ff:ff:ff:ff',
                                                                psrc=dstip, pdst=dstip)
            sendp(pkt, iface=ifname, verbose=False)

        elif platform.system() == "Windows":
            mac = get_mac_address(ifname)
            # 得到win网卡mac
            from kamene_interface import kamene_iface
            winifname = kamene_iface(ifname)
            # 得到win网卡名称（详细信息里的 '描述' 名称）
            pkt = Ether(src=mac, dst='ff:ff:ff:ff:ff:ff') / ARP(op=2, hwsrc=mac,
                                                                hwdst='ff:ff:ff:ff:ff:ff',
                                                                psrc=dstip, pdst=dstip)
            sendp(pkt, iface=winifname, verbose=False)

        time.sleep(1)
        print(a, flush=False)


if __name__ == '__main__':
    arp_reply('192.168.111.4', 'VMware Network Adapter VMnet1')

