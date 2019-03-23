# -*- coding=utf-8 -*-

import logging
logging.getLogger("kamene.runtime").setLevel(logging.ERROR)  # 清除报错
from kamene.all import *
from get_ifname import get_ifname
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


if __name__ == '__main__':
    print(kamene_iface('VMware Network Adapter VMnet1'))


