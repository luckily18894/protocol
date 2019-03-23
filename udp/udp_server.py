# -*- coding=utf-8 -*-

import socket
import sys
import struct
import pickle
import hashlib


address = ("127.0.0.1", 6666)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(address)

print('UDP服务器就绪！等待客户数据！')
while True:
    try:
        recv_source_data = s.recvfrom(2048)
        # print(recv_source_data)
        addr = recv_source_data[1]
        # 得到地址和端口
        md5_recv = recv_source_data[0][-32:]
        # 得到打包时计算的md5
        data = recv_source_data[0][12:-32]
        # 得到被发送的数据
        head = recv_source_data[0][:12]
        # 得到包头部

        m = hashlib.md5()
        m.update(head + data)
        md5_value = m.hexdigest()

        version, pkt_type, seq_id, length = struct.unpack('!hhii', head)

        if md5_recv == md5_value.encode():
            print('=' * 40)
            print('{0:<8}:{1:<}'.format('数据来自于', str(addr)))
            print('{0:<8}:{1:<}'.format('数据序号为', seq_id))
            print('{0:<8}:{1:<}'.format('数据长度为', length))
            print('{0:<8}:{1:<}'.format('数据内容为', str(pickle.loads(data))))
    except KeyboardInterrupt:
        sys.exit()

