# -*- coding=utf-8 -*-

import pyshark
from pymongo import *

# 连接数据库
client = MongoClient('mongodb://luckily18894:luCKi1y18894@192.168.1.110:27017/pythondb')
db = client['pythondb']
db.secie.remove()


def read_pcap_to_db(file):
    cap = pyshark.FileCapture(file, keep_packets=False)  # 打开PCAP文件

    for pkt in cap:  # 遍历包
        pkt_dict, res = {}, {}

        # 取出每一层，将其内容压成字典
        for layer in pkt.__dict__.get('layers'):
            pkt_dict.update(layer.__dict__.get('_all_fields'))

        # 将key中的 . 替换成 _    eth.addr ——> eth_addr
        for key, value in pkt_dict.items():
            res[key.replace('.', '_')] = value

        # 入库
        db.pktinfo.insert_one(res)


if __name__ == '__main__':
    read_pcap_to_db('test.pcap')

