# -*- coding=utf-8 -*-

import logging

logging.getLogger("kamene.runtime").setLevel(logging.ERROR)
import re
from kamene.all import *
from tools.interface_tools import kamene_iface

qyt_string = b''


def reset_tcp(pkt):
    # 本代码主要任务: 对传入的数据包,发送TCP Rest进行会话重置
    source_mac = pkt[Ether].fields['src']
    destination_mac = pkt[Ether].fields['dst']
    source_ip = pkt[IP].fields['src']
    destination_ip = pkt[IP].fields['dst']
    source_port = pkt[TCP].fields['sport']
    destination_port = pkt[TCP].fields['dport']
    seq_sn = pkt[TCP].fields['seq']
    ack_sn = pkt[TCP].fields['ack']

    a = Ether(src=source_mac, dst=destination_mac) / IP(src=source_ip, dst=destination_ip) / TCP(dport=destination_port,
                                                                                                 sport=source_port,
                                                                                                 flags=4, seq=seq_sn)
    b = Ether(src=destination_mac, dst=source_mac) / IP(src=destination_ip, dst=source_ip) / TCP(dport=source_port,
                                                                                                 sport=destination_port,
                                                                                                 flags=4, seq=ack_sn)
    sendp(a,
          iface=global_if,
          verbose=False)
    sendp(b,
          iface=global_if,
          verbose=False)


def telnet_monitor_callback(pkt):
    # 通过对Telnet会话数据的拼接,判断是否出现dis cu字段, 如果出现重置会话
    global qyt_string
    try:
        if pkt.getlayer(TCP).fields['dport'] == 23:
            if pkt.getlayer(Raw).fields['load'].decode():
                qyt_string = qyt_string + pkt.getlayer(Raw).fields['load']  # 不断提取数据,拼接到qyt_string
    except:
        pass

    if re.match(b'(.*\r.*)*di.*\s+cu.*', qyt_string):  # 如果出现dis cu字段,就Rest踢掉此会话
        reset_tcp(pkt)


def telnet_rst(user_filter, ifname):
    # 本代码主要任务: 使用过滤器捕获数据包, 把捕获的数据包交给telnet_monitor_callback进行处理
    global global_if
    global_if = kamene_iface(ifname)
    PTKS = sniff(prn=telnet_monitor_callback,
                 filter=user_filter,
                 store=1,
                 iface=global_if,
                 timeout=10)
    wrpcap("qytang_day18.pcap", PTKS)
    print(qyt_string)


if __name__ == "__main__":
    while True:
        try:
            # telnet_rst("tcp port 23 and ip host 192.168.1.107", "VMware Network Adapter VMnet1")
            telnet_rst("tcp port 23 and ip host 192.168.1.107", "ens33")
        except KeyboardInterrupt:
            print('stopped')


