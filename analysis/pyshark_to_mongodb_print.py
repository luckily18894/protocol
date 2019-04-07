# -*- coding=utf-8 -*-

import pyshark
from pymongo import *

# 连接数据库
# client = MongoClient('mongodb://luckily18894:luCKi1y18894@192.168.1.110:27017/pythondb')
# db = client['pythondb']
# db.secie.remove()


def read_pcap_to_db(pcap_file):
    cap = pyshark.FileCapture(pcap_file, keep_packets=False)  # 打开PCAP文件
    num = 1
    for pkt in cap:  # 遍历包
        # 将包内容压成字典
        pkt_dict = pkt.__dict__

        # layers 为除frame的各层信息的列表
        layers_list = pkt_dict['layers']

        dict1, dict2, dict3 = {}, {}, {}
        for layer in layers_list:  # 取得除各层的内容
            layer_name = layer._layer_name

            # 提取每层 所包含的字段名
            for field_name in layer.field_names:
                # 取得各字段的内容并存入字典
                res = getattr(layer, field_name)
                print(res)
                dict1[field_name] = res
                # print(res)
            # 字典逐步向上拼接
                dict2[layer_name] = dict1
        pkt_dict['layers'] = dict2
        # print(pkt.eth.field_names)
        #
        # # 取得frame的信息 同上
        # frame_info = pkt_dict['frame_info']
        # for field_name in frame_info.field_names:
        #     res = getattr(frame_info, field_name)
        #     dict3[field_name] = res
        # pkt_dict['frame_info'] = dict3
        #
        # # 写入数据库
        # db.secie.insert_one(pkt_dict)
        # print(num)
        # num += 1



    # try:
    #     print(pkt.layers)
        # print(dir(pkt.layers.append))
    # except:
    #     pass
    # attribute_list = dir(pkt)[32:]
    # # print(attribute_list)
    # for a in attribute_list:  # 遍历各属性的值
        # if type(a) == list:
        #     print('1')
        # else:
        #     res = getattr(pkt, a)
        #     print(a, type(res), res)
    #
    #     print(res)
    #     res = getattr(pkt, a)  # 获取pkt中 a这个属性的值
    # #
    #     # 写入数据库
    #     obj = {a: res}
    #     print(a, res)
        # db.secie.insert_one(obj)



# if __name__ == '__main__':
#     i = 1
#     for pkt in get_tcp_stream('dos.pcap', 10):
#         print('='*30, i, '='*30)
#         pkt.pretty_print()
#         i += 1
#
if __name__ == '__main__':
    read_pcap_to_db('test.pcap')

    # 使用matplot进行图形化展示
    # import matplotlib.pyplot as plt
    # import matplotlib.ticker as mtick
    #
    # method, hits = [], []
    # for x, y in method_dict.items():
    #     method.append(x)
    #     hits.append(y)
    #
    # fig = plt.figure(figsize=(5, 5))
    # ax = fig.add_subplot(111)  # 一共一行, 每行一图, 第一图
    # plt.bar(method, hits, width=0.5)  # 设置为竖向图
    # ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%d'))  # 设置Y轴格式
    #
    # plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文
    # plt.title('抓包Method数量')  # 主题
    # plt.xlabel('Method')  # X轴注释
    # plt.ylabel('数量')  # Y轴注释
    #
    # plt.show()



# dir 不同类型包 所有显示字段一览
# pkt
# ['__class__', '__contains__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattr__', '__getattribute__', '__getitem__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setstate__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_packet_string', 'captured_length', 'eth', 'frame_info', 'get_multiple_layers', 'get_raw_packet', 'highest_layer', 'http', 'interface_captured', 'ip', 'layers', 'length', 'number', 'pretty_print', 'show', 'sniff_time', 'sniff_timestamp', 'tcp', 'transport_layer']
# ip
# ['', 'DATA_LAYER', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattr__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setstate__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_all_fields', '_field_prefix', '_get_all_field_lines', '_get_all_fields_with_alternates', '_get_field_or_layer_repr', '_get_field_repr', '_layer_name', '_sanitize_field_name', 'addr', 'checksum', 'checksum_status', 'dsfield', 'dsfield_dscp', 'dsfield_ecn', 'dst', 'dst_host', 'field_names', 'flags', 'flags_df', 'flags_mf', 'flags_rb', 'frag_offset', 'get', 'get_field', 'get_field_by_showname', 'get_field_value', 'hdr_len', 'host', 'id', 'layer_name', 'len', 'pretty_print', 'proto', 'raw_mode', 'src', 'src_host', 'ttl', 'version']
# tcp
# ['DATA_LAYER', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattr__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setstate__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_all_fields', '_field_prefix', '_get_all_field_lines', '_get_all_fields_with_alternates', '_get_field_or_layer_repr', '_get_field_repr', '_layer_name', '_sanitize_field_name', 'ack', 'analysis', 'analysis_bytes_in_flight', 'analysis_initial_rtt', 'analysis_push_bytes_sent', 'checksum', 'checksum_status', 'dstport', 'field_names', 'flags', 'flags_ack', 'flags_cwr', 'flags_ecn', 'flags_fin', 'flags_ns', 'flags_push', 'flags_res', 'flags_reset', 'flags_str', 'flags_syn', 'flags_urg', 'get', 'get_field', 'get_field_by_showname', 'get_field_value', 'hdr_len', 'layer_name', 'len', 'nxtseq', 'payload', 'port', 'pretty_print', 'raw_mode', 'seq', 'srcport', 'stream', 'urgent_pointer', 'window_size', 'window_size_scalefactor', 'window_size_value']
# http
# ['', 'DATA_LAYER', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattr__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setstate__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_all_fields', '_field_prefix', '_get_all_field_lines', '_get_all_fields_with_alternates', '_get_field_or_layer_repr', '_get_field_repr', '_layer_name', '_sanitize_field_name', '_ws_expert', '_ws_expert_group', '_ws_expert_message', '_ws_expert_severity', 'accept', 'accept_encoding', 'accept_language', 'chat', 'connection', 'cookie', 'cookie_pair', 'field_names', 'get', 'get_field', 'get_field_by_showname', 'get_field_value', 'host', 'layer_name', 'pretty_print', 'raw_mode', 'request', 'request_full_uri', 'request_line', 'request_method', 'request_number', 'request_uri', 'request_uri_path', 'request_uri_query', 'request_uri_query_parameter', 'request_version', 'user_agent']
