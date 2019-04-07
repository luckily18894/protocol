# -*- coding=utf-8 -*-

import pyshark

pkt_list = []

cap = pyshark.FileCapture('cap1.pcap', keep_packets=False, display_filter='http')

method_dict = {}


def print_highest_layer(pkt):
    # 本代码的主要任务: 对HTTP流量进行分析,找到特定method的请求数量
    try:
        # 字典数据结构如下
        # 键为method, 值为数量
        counts = method_dict.get(pkt.http.request_method, 0)
        counts += 1
        method_dict[pkt.http.request_method] = counts
    except:
        pass

# 应用函数到数据包
cap.apply_on_packets(print_highest_layer)
print(method_dict)


if __name__ == '__main__':
    # 使用matplot进行图形化展示
    import matplotlib.pyplot as plt
    import matplotlib.ticker as mtick

    method, hits = [], []
    for x, y in method_dict.items():
        method.append(x)
        hits.append(y)

    fig = plt.figure(figsize=(5, 5))
    ax = fig.add_subplot(111)  # 一共一行, 每行一图, 第一图
    plt.bar(method, hits, width=0.5)  # 设置为竖向图
    ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%d'))  # 设置Y轴格式

    plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文
    plt.title('抓包Method数量')  # 主题
    plt.xlabel('Method')  # X轴注释
    plt.ylabel('数量')  # Y轴注释

    plt.show()


