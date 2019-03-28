# -*- coding=utf-8 -*-

import sqlite3
from dateutil import parser
import matplotlib.pyplot as plt
import matplotlib.dates as mdate
import matplotlib.ticker as mtick
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['font.family'] = 'sans-serif'


def read_print_list(dbname):
    # 连接数据库并读取
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()
    cursor.execute('select time, cpu from cpudb')
    yourresults = cursor.fetchall()

    return yourresults


def cpu_draw(dbname):
    # 将数据库中的数据取出，分成 时间、使用率 2个列表
    time_list = []
    cpu_list = []
    for time, cpu in read_print_list(dbname):
        time_list.append(parser.parse(time))
        cpu_list.append(cpu)

    # 调节图形大小，宽，高
    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111)  # 一共一行, 每行一图, 第一图

    plt.title('路由器CPU利用率')
    plt.xlabel('采集时间')
    plt.ylabel('CPU利用率')

    fig.autofmt_xdate()  # 当x轴太拥挤的时候可以让他自适应

    ax.xaxis.set_major_formatter(mdate.DateFormatter("%H:%M:%S"))  # 设置X轴格式
    ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%d%%'))  # 设置Y轴格式
    # 传入数据,time为X轴,cpu为Y轴
    ax.plot(time_list, cpu_list, linestyle='solid', color='r', label='CPU利用率')
    ax.set_ylim(bottom=0, top=50)  # 设置Y轴 最小值 和 最大值
    ax.legend(loc='upper right')  # 设置说明的位置

    plt.show()


if __name__ == '__main__':
    cpu_draw('cpu_usage.sqlite')


