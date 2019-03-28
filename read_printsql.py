# -*- coding=utf-8 -*-

import sqlite3
from dateutil import parser
import matplotlib.pyplot as plt
import matplotlib.dates as mdate
import matplotlib.ticker as mtick
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['font.family'] = 'sans-serif'


def cpu_show(dbname):
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()

    cursor.execute("select time, cpu from routerdb")
    yourresults = cursor.fetchall()

    time_list = []
    cpu_list = []
    for time_cpu in yourresults:
        time_list.append(time_cpu[0])
        cpu_list.append(time_cpu[1])

    # 转换字符串到时间对象
    time_list = [parser.parse(i) for i in time_list]

    # 调节图形大小，宽，高
    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111)  # 一共一行, 每行一图, 第一图

    plt.title('路由器CPU利用率')
    plt.xlabel('采集时间')
    plt.ylabel('CPU利用率')

    fig.autofmt_xdate()  # 当x轴太拥挤的时候可以让他自适应

    # 格式化X轴
    # ax.xaxis.set_major_formatter(mdate.DateFormatter('%Y-%m-%d %H:%M:%S'))#设置时间标签显示格式
    ax.xaxis.set_major_formatter(mdate.DateFormatter("%H:%M:%S"))  # 设置时间标签显示格式
    # 格式化Y轴
    # ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.2f%%'))#格式化Y轴
    ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%d%%'))  # 格式化Y轴
    # 传入数据,time为X轴,cpu为Y轴
    ax.plot(time_list, cpu_list, linestyle='solid', color='r', label='CPU利用率')
    # 设置Y轴 最小值 和 最大值
    ax.set_ylim(bottom=0, top=100)

    ax.legend(loc='upper right')  # 设置说明的位置
    plt.show()


def mem_show(dbname):
    # 连接数据库
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()
    # 提取时间,MEM使用量和空闲量
    cursor.execute("select time, memu, memf from routerdb")
    yourresults = cursor.fetchall()

    time_list = []
    mem_list = []

    # 把结果写入time_list和cpu_list的列表
    for time_mem in yourresults:
        time_list.append(time_mem[0])

        mem_list.append((time_mem[1]/(time_mem[1] + time_mem[2]))*100)

    # 转换字符串到时间对象
    time_list = [parser.parse(i) for i in time_list]

    # 调节图形大小，宽，高
    fig = plt.figure(figsize=(6, 6))
    # 一共一行, 每行一图, 第一图
    ax = fig.add_subplot(111)

    # 添加主题和注释
    plt.title('路由器MEM利用率')
    plt.xlabel('采集时间')
    plt.ylabel('MEM利用率')

    fig.autofmt_xdate()  # 当x轴太拥挤的时候可以让他自适应

    # 格式化X轴
    # ax.xaxis.set_major_formatter(mdate.DateFormatter('%Y-%m-%d %H:%M:%S'))#设置时间标签显示格式
    ax.xaxis.set_major_formatter(mdate.DateFormatter("%H:%M:%S"))  # 设置时间标签显示格式
    # 格式化Y轴
    # ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.2f%%'))#格式化Y轴
    ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%d%%'))  # 格式化Y轴
    # 传入数据,time为X轴,cpu为Y轴
    ax.plot(time_list, mem_list, linestyle='solid', color='r', label='MEM利用率')
    # 设置Y轴 最小值 和 最大值
    ax.set_ylim(bottom=0, top=100)

    # 设置说明的位置
    ax.legend(loc='upper left')
    # 显示图像
    plt.show()


if __name__ == '__main__':
    cpu_show("cpu_usage.sqlite")
    mem_show("cpu_usage.sqlite")


