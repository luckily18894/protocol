# -*- coding=utf-8 -*-

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from pymongo import *

client = MongoClient('mongodb://luckily18894:luCKi1y18894@192.168.1.10:27017/pythondb')
db = client['pythondb']


pkt_dict = {}
for x in db.pktinfo.find({'tcp_flags': '2'}):
    count = pkt_dict.get((x.get('ip_src'), x.get('ip_dst'), x.get('tcp_dstport')), 0)
    pkt_dict[(x.get('ip_src'), x.get('ip_dst'), x.get('tcp_dstport'))] = count + 1

sorted_dict_key = sorted(pkt_dict, key=lambda k: pkt_dict[k], reverse=True)
sorted_dict_key_top3 = ['SRC:' + x[0] + ' ' + 'DST:' + x[1] + ' ' + 'PORT:' + x[2] for x in sorted_dict_key[:5]]
sorted_counts = []
for x in sorted_dict_key[:5]:
    sorted_counts.append(pkt_dict.get(x))


fig = plt.figure(figsize=(8, 8))

ax = fig.add_subplot(111)  # 一共一行, 每行一图, 第一图
plt.bar(sorted_dict_key_top3, sorted_counts, width=0.5)  # 设置为竖向图
ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%d'))  # 设置Y轴格式

plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文
plt.title('连接会话数')  # 主题
plt.xlabel('源目地址 端口号')  # X轴注释
plt.ylabel('会话数')  # Y轴注释
fig.autofmt_xdate()  # 当x轴太拥挤的时候可以让他自适应  放到最后才有效。。
plt.show()


pkt_dict = {}
for a in db.pktinfo.find({'arp_opcode': '1'}):  # 找到ARP请求的记录
    count = pkt_dict.get(a.get('arp_src_hw_mac'), 0)
    pkt_dict[a.get('arp_src_hw_mac')] = count + 1
name_list, size_list = [], []
for key in pkt_dict:
    name_list.append(key+'\n'+str(pkt_dict[key])+'个')
    size_list.append(pkt_dict[key])

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['font.family'] = 'sans-serif'

plt.figure(figsize=(6, 6))

explode = [0, 0, 0.1]
# 将某部分爆炸出来，使用括号，将第一块分割出来，数值的大小是分割出来的 与其他两块的间隙
patches, label_text, percent_text = plt.pie(size_list,
                                            explode=explode,
                                            labels=name_list,
                                            labeldistance=1.1,
                                            autopct='%d%%',
                                            shadow=True,
                                            startangle=90, pctdistance=0.6)
for l in label_text:
    l.set_size = 30
for p in percent_text:
    p.set_size = 20
# 设置x,y轴刻度一致,这样饼图才能是圆的
plt.axis('equal')
plt.title('ARP请求源及个数占比')
# plt.legend()
plt.show()

