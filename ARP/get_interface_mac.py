# -*- coding=utf-8 -*-

import netifaces
import platform
# import pprint
# pp = pprint.PrettyPrinter(indent=4)


def get_mac_address(ifname):
    if platform.system() == "Linux":
        # pp.pprint(netifaces.ifaddresses(ifname))
        # print(netifaces.AF_LINK)
        return netifaces.ifaddresses(ifname)[netifaces.AF_LINK][0]['addr']
    elif platform.system() == "Windows":
        from win_interface_name import win_from_name_get_id
        if_id = win_from_name_get_id(ifname)
        return netifaces.ifaddresses(if_id)[netifaces.AF_LINK][0]['addr']
    else:
        print('操作系统不支持,本脚本只能工作在Windows或者Linux环境!')


if __name__ == '__main__':
    print(get_mac_address("VMware Network Adapter VMnet1"))
    # print(get_mac_address("ens33"))


