# -*- coding=utf-8 -*-

from matplotlib import pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['font.family'] = 'sans-serif'


def mat_line(cpu_usage_list1, cpu_usage_list2):
    fig = plt.figure(figsize=(6, 6))  # 调节图形大小，宽，高
    ax = fig.add_subplot(211)  # 一共一行, 每行一图, 第一图

    # 处理X轴时间格式
    import matplotlib.dates as mdate
    # 设置时间标签显示格式
    ax.xaxis.set_major_formatter(mdate.DateFormatter('%H:%M'))
    # ax.xaxis.set_major_formatter(mdate.DateFormatter('%Y-%m-%d %H:%M:%S'))

    # 处理Y轴百分比格式
    import matplotlib.ticker as mtick
    ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%d%%'))

    # 把cpu_usage_list的数据,拆分为x轴的时间,与y轴的利用率
    x1 = []
    y1 = []
    x2 = []
    y2 = []
    for time, cpu in cpu_usage_list1:
        x1.append(time)
        y1.append(cpu)
    for time, cpu in cpu_usage_list2:
        x2.append(time)
        y2.append(cpu)

    # 添加主题和注释
    plt.title('路由器CPU利用率')
    plt.xlabel('采集时间')
    plt.ylabel('CPU利用率')

    fig.autofmt_xdate()  # 当x轴太拥挤的时候可以让他自适应

    # 实线红色
    ax.plot(x1, y1, linestyle='solid', color='r', label='R1')
    # 如果你有两套数据,完全可以在一幅图中绘制双线
    ax.plot(x2, y2, linestyle='dashed', color='b', label='R2')

    # # 虚线黑色
    # ax.plot(x1, y1, linestyle='dashed', color='b', label='R1')

    ax.legend(loc='upper left')  # 设置说明的位置
    # plt.savefig('result1.png')  # 保存到图片
    plt.show()  # 绘制图形


if __name__ == "__main__":
    import random
    import datetime

    cpu1 = []
    cpu2 = []
    for a in range(-12, 13):
        time1 = (datetime.datetime.now() + datetime.timedelta(hours=a))
        usage1 = random.randint(1, 100)
        cpu1.append((time1, usage1))

    for b in range(-12, 13):
        time2 = (datetime.datetime.now() + datetime.timedelta(hours=b))
        usage2 = random.randint(1, 100)
        cpu2.append((time2, usage2))

    mat_line(cpu1, cpu2)

