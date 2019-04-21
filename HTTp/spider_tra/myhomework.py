# -*- coding=utf-8 -*-

from bs4 import BeautifulSoup
import requests
import re
from pymongo import *
import matplotlib.pyplot as plt


def read_header(head_file):  # 可将头部信息的文本文件转换成字典
    header_dict = {}

    header_txt = open(head_file)
    for header in header_txt.readlines():
        key, val = header.strip().split(':')
        header_dict[key.strip()] = val.strip()

    return header_dict


def get_my_homework(head_file):  # 得到作业的页面
    client = requests.session()
    # homework页面URL
    url = 'https://qytsystem.qytang.com/python_enhance/python_enhance_homework'

    # 获取homework页面
    homework = client.get(url, headers=read_header(head_file))

    # lxml HTML 解析器
    homework_soup = BeautifulSoup(homework.text, 'lxml')

    # 返回收到的页面   .prettify是自动缩进，好看点（无所谓）。
    # return homework_soup.prettify()
    return homework_soup


def soupinfo_to_db():
    homework_soup = get_my_homework('header.txt')

    dictdb = {}
    l1, l2, l3, l4, l5 = [], [], [], [], []

    table = homework_soup.find('table', class_="table table-bordered")
    for a in table.find_all('th', class_='text-center'):
        l1.append(a.text)
    # print(l1)

    tbody = homework_soup.find('tbody', class_="text-center")
    for a in tbody:
        if a != '\n':
            l2.append(a)

    for a in l2:
        for b in a.find_all('td'):

            try:
                if b.find('a').get('title') == '下载此作业':
                    l3.append('下载此作业  https://qytsystem.qytang.com{0}'.format(b.find('a').get('href')))

                elif b.find('a').get('title') == '作业已经被老师检查不能被删除':
                    l3.append('作业已经被老师检查不能被删除')

                elif b.find('a').get('title') == '删除此作业':
                    l3.append('删除此作业  https://qytsystem.qytang.com{0}'.format(b.find('a').get('href')))

            except AttributeError:
                l3.append(b.text)

        l4.append(l3)
        l3 = []  # 列表清空，准备下一次循环

    # print(l4)

    for a in l4:
        dictdb = dict(zip(l1, a))
        l5.append(dictdb)
    # print(l5)

    # 入库
    client = MongoClient('mongodb://luckily18894:luCKi1y18894@192.168.1.10:27017/pythondb')
    db = client['pythondb']

    db.secie.insert_many(l5)

    print('读取页面并写入成功')


def db_draw(key_for_draw, title):
    client = MongoClient('mongodb://luckily18894:luCKi1y18894@192.168.1.10:27017/pythondb')
    db = client['pythondb']

    res_dict = {}
    for a in db.secie.find():  # 找到ARP请求的记录
        count = res_dict.get(a.get(key_for_draw), 0)
        res_dict[a.get(key_for_draw)] = count + 1

    name_list, size_list = [], []
    for key in res_dict:
        name_list.append(key)
        size_list.append(res_dict[key])
    # print(name_list)
    # print(size_list)

    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['font.family'] = 'sans-serif'

    plt.figure(figsize=(6, 6))

    # explode = [0, 0, 0.1]
    # 将某部分爆炸出来，使用括号，将第一块分割出来，数值的大小是分割出来的 与其他两块的间隙
    patches, label_text, percent_text = plt.pie(size_list,
                                                # explode=explode,
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
    plt.title(title)
    plt.legend()
    plt.show()


if __name__ == "__main__":
    # soupinfo_to_db()
    db_draw('课程', '课程作业分布图')

