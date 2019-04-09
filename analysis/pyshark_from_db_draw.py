# -*- coding=utf-8 -*-

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from pymongo import *

client = MongoClient('mongodb://luckily18894:luCKi1y18894@192.168.1.110:27017/pythondb')
db = client['pythondb']


dos_dict = {}
for x in db.pktinfo.find({'tcp_flags': '2'}):
    counts = dos_dict.get((x.get('ip_src'), x.get('ip_dst'), x.get('tcp_dstport')), 0)
    dos_dict[(x.get('ip_src'), x.get('ip_dst'), x.get('tcp_dstport'))] = counts + 1

sorted_dict_key = sorted(dos_dict, key=lambda k: dos_dict[k], reverse=True)
sorted_dict_key_top3 = ['SRC:' + x[0] + ' ' + 'DST:' + x[1] + ' ' + 'PORT:' + x[2] for x in sorted_dict_key[:5]]
sorted_counts = []
for x in sorted_dict_key[:5]:
    sorted_counts.append(dos_dict.get(x))


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



