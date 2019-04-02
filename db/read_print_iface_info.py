# -*- coding=utf-8 -*-

import numpy as np
from pymongo import *
import datetime
from matplotlib import pyplot as plt
import matplotlib.dates as mdate
import matplotlib.ticker as mtick

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['font.family'] = 'sans-serif'


def serch_info_from_db(ifnumber, direction, last_mins):
    client = MongoClient('mongodb://luckily18894:luCKi1y18894@192.168.1.110:27017/pythondb')
    db = client['pythondb']

    starttime = datetime.datetime.now() - datetime.timedelta(minutes=last_mins)

    if_bytes_list, record_time_list = [], []
    for obj in db.secie.find({'if_name': 'GigabitEthernet0/0/{0}'.format(ifnumber), 'record_time': {'$gte': starttime}}):
        if_bytes_list.append(obj['{0}_bytes'.format(direction)])
        record_time_list.append(obj['record_time'])
        # print(obj)
    # print(if_bytes_list)
    # print(record_time_liste)

    # 计算两次获取的字节数的差值
    diff_if_bytes_list = list(np.diff(if_bytes_list))
    # 计算两次时间对象的秒数差值
    diff_record_time_list = [x.seconds for x in np.diff(record_time_list)]
    # 计算速率
    speed_list = list(map(lambda x: round(((x[0] * 8) / (1000 * x[1])), 2),
                          zip(diff_if_bytes_list, diff_record_time_list)))

    return record_time_list[1:], speed_list


def mem_draw(ifnumber, direction, last_mins):
    # 从数据库中获取信息
    time_list, speed_list = serch_info_from_db(ifnumber, direction, last_mins)

    # 调节图形大小，宽，高
    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111)  # 一共一行, 每行一图, 第一图

    plt.title('GigabitEthernet0/0/{0} {1}方向 近{2}分钟速率'.format(ifnumber, direction, last_mins))
    plt.xlabel('采集时间')
    plt.ylabel('速率kbps')

    fig.autofmt_xdate()  # 当x轴太拥挤的时候可以让他自适应

    ax.xaxis.set_major_formatter(mdate.DateFormatter("%H:%M:%S"))  # 设置X轴格式
    ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.0f'))  # 设置Y轴格式
    # 传入数据,time为X轴,cpu为Y轴
    ax.plot(time_list, speed_list, linestyle='solid', color='b', label='R1')
    ax.set_ylim(bottom=0, top=100)  # 设置Y轴 最小值 和 最大值
    ax.legend(loc='upper right')  # 设置说明的位置

    plt.show()


if __name__ == '__main__':
    # print(serch_info_from_db(1, 'in', 120))
    mem_draw(2, 'out', 1)



