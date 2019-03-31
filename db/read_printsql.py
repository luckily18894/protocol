# -*- coding=utf-8 -*-

import pg8000
from datetime import datetime
from dateutil import parser
import matplotlib.pyplot as plt
import matplotlib.dates as mdate
import matplotlib.ticker as mtick
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['font.family'] = 'sans-serif'


def read_print_list(start_time, endtime):
    # 连接数据库并读取
    conn = pg8000.connect(host='192.168.1.10', user='luckily18894', password='luCKi1y18894', database='pythondb')
    cursor = conn.cursor()
    cursor.execute("select * from memorydb WHERE record_time >='{0}' AND record_time < '{1}'".format(start_time, endtime))
    yourresults = cursor.fetchall()

    return yourresults


def mem_draw(start_time, endtime):
    # 将数据库中的数据取出，分成 时间、使用率 2个列表
    time_list = []
    mem_list = []
    for a in read_print_list(start_time, endtime):
        time_list.append(a[3])
        mem_list.append(float(a[2]))
    print(time_list)
    # 调节图形大小，宽，高
    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111)  # 一共一行, 每行一图, 第一图

    plt.title('路由器内存利用率')
    plt.xlabel('采集时间')
    plt.ylabel('内存利用率')

    fig.autofmt_xdate()  # 当x轴太拥挤的时候可以让他自适应

    ax.xaxis.set_major_formatter(mdate.DateFormatter("%H:%M:%S"))  # 设置X轴格式
    ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.2f%%'))  # 设置Y轴格式
    # 传入数据,time为X轴,cpu为Y轴
    ax.plot(time_list, mem_list, linestyle='solid', color='b', label='内存利用率')
    ax.set_ylim(bottom=0, top=100)  # 设置Y轴 最小值 和 最大值
    ax.legend(loc='upper right')  # 设置说明的位置

    plt.show()


if __name__ == '__main__':
    start = datetime(2019, 3, 31, 22, 00, 0, 000000)
    end = datetime(2019, 3, 31, 22, 20, 0, 000000)

    mem_draw(start, end)
    # print(read_print_list(start, end))

