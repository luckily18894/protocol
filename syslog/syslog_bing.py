# -*- coding=utf-8 -*-

import sqlite3
from matplotlib import pyplot as plt

logsourse = {0: '01OSPF', 1: 'Link', 2: 'sys'}


def syslog_show(dbname):
    # 连接数据库
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()

    cursor.execute("select log_source as sourse,COUNT(*) as count from syslogdb group by log_source")
    yourresults = cursor.fetchall()

    level_list, count_list = [], []
    print(yourresults)
    for level_count in yourresults:
        level_list.append(level_count[0])
        count_list.append(level_count[1])

    print(level_list)
    # print([float(count) for count in count_list])

    plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文
    #调节图形大小，宽，高
    plt.figure(figsize=(6, 6))

    # 使用count_list的比例来绘制饼图
    # 使用level_list作为注释
    patches, l_text, p_text = plt.pie(count_list,
                                      labels=level_list,
                                      labeldistance=1.1,
                                      autopct='%3.1f%%',
                                      shadow=False,
                                      startangle=90,
                                      pctdistance=0.6)

    #labeldistance，文本的位置离远点有多远，1.1指1.1倍半径的位置
    #autopct，圆里面的文本格式，%3.1f%%表示小数有三位，整数有一位的浮点数
    #shadow，饼是否有阴影
    #startangle，起始角度，0，表示从0开始逆时针转，为第一块。一般选择从90度开始比较好看
    #pctdistance，百分比的text离圆心的距离
    #patches, l_texts, p_texts，为了得到饼图的返回值，p_texts饼图内部文本的，l_texts饼图外label的文本

    #改变文本的大小
    #方法是把每一个text遍历。调用set_size方法设置它的属性
    for t in l_text:
        t.set_size = 30
    for t in p_text:
        t.set_size = 20
    # 设置x，y轴刻度一致，这样饼图才能是圆的
    plt.axis('equal')
    plt.title('SYSLOG严重级别分布图')  # 主题
    plt.legend()
    plt.show()


if __name__ == '__main__':
    syslog_show("syslog.sqlite")


