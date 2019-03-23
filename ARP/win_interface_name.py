# -*- coding=utf-8 -*-

import netifaces as ni
import winreg as wr


def get_connection_name_from_guid(iface_guids):
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
    x = ni.interfaces()
    # print(x)
    return get_connection_name_from_guid(x).get(ifname)


if __name__ == '__main__':
    print(win_from_name_get_id("VMware Network Adapter VMnet1"))


