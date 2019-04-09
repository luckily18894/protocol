# -*- coding=utf-8 -*-

import pg8000
from datetime import datetime
from dateutil import parser
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['font.family'] = 'sans-serif'
import re


def read_print_list(start_time, endtime):
    # 连接数据库并读取
    conn = pg8000.connect(host='192.168.1.10', user='luckily18894', password='luCKi1y18894', database='pythondb')
    cursor = conn.cursor()
    cursor.execute("select * from memorydb WHERE record_time >='{0}' AND record_time < '{1}'".format(start_time, endtime))
    yourresults = cursor.fetchall()
    print(yourresults)
    return yourresults


def mem_draw(start_time, endtime):
    # 将数据库中的数据取出，分成 时间、使用率 2个列表
    time_list, mem_list, a = [], [], []
    for n in read_print_list(start_time, endtime):
        time_list.append(n[3])
        mem_list.append(float(n[2]))
    print(time_list)
    return time_list


if __name__ == '__main__':
    start = datetime(2019, 3, 31, 22, 00, 0, 000000)
    end = datetime(2019, 3, 31, 22, 20, 0, 000000)
    mem_draw(start, end)
    # # mem_draw(start, end)
    read_print_list(start, end)
    # import time
    # time = mem_draw(start, end)
    # print(time)
    # list1 = []
    # for a in time:
    #     list1.append(parser.parse(a.strftime("%H:%M:%S")))
    #     # print(a)
    # print(list1)



