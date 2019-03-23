# -*- coding=utf-8 -*-

import socket
import pickle
import struct
import hashlib


def udp_send_data(ip, port, data_list):
    addresss = (ip, port)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    version = 1
    pkt_type = 1
    seq_id = 1

    for x in data_list:
        send_data = pickle.dumps(x)
        head = struct.pack('!hhii', version, pkt_type, seq_id, len(send_data))

        m = hashlib.md5()
        m.update(head + send_data)
        md5_value = m.hexdigest()

        s.sendto(head + send_data + md5_value.encode(), addresss)
        seq_id += 1
    s.close()


if __name__ == '__main__':
    user_data = ['乾颐堂', [1, 'qytang', 3], {'qytang': 1, 'test': 3}]
    udp_send_data('127.0.0.1', 6666, user_data)

