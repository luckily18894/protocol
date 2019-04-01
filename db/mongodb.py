# -*- coding=utf-8 -*-

import os
import time
from pymongo import *
import datetime
from pysnmp.hlapi import *


def snmpv2_get(ip, community, oid, port=161):
    # varBinds是列表，列表中的每个元素的类型是ObjectType（该类型的对象表示MIB variable）
    errorIndication, errorStatus, errorindex, varBinds = next(
        getCmd(SnmpEngine(),
               CommunityData(community),  # 配置community
               UdpTransportTarget((ip, port)),  # 配置目的地址和端口号
               ContextData(),
               ObjectType(ObjectIdentity(oid))))  # 读取的OID
    # 错误处理
    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print('%s at %s' % (errorStatus, errorindex and varBinds[int(errorindex) - 1][0] or '?'))
    # 如果返回结果有多行,需要拼接后返回
    result = ''

    for varBind in varBinds:
        result = result + varBind.prettyPrint()  # 返回结果
    # print(result)
    # 返回的为一个元组,OID与字符串结果
    return result.split("=")[0].strip(), result.split("=")[1].strip()


def get_info_writedb(ip, rocommunity):
    # 连接psql数据库并创建表项
    client = MongoClient('mongodb://luckily18894:luCKi1y18894@192.168.1.10:27017/pythondb')
    db = client['pythondb']
    db.secie.remove()

    while True:
        try:
            # 获取内存总量
            memory_all = snmpv2_get(ip, rocommunity, '1.3.6.1.4.1.2011.6.3.5.1.1.2.0.0.0', port=161)[1]
            # 获取内存空闲量
            memory_free = snmpv2_get(ip, rocommunity, '1.3.6.1.4.1.2011.6.3.5.1.1.3.0.0.0', port=161)[1]
            # 计算出内存使用率,保留两位小数
            memory_used = int(memory_all) - int(memory_free)
            memory_usage = '{:.2f}'.format((memory_used / int(memory_all) * 100))

            # 把数据写入数据库
            record = {'memoryusage': '{0}'.format(memory_usage), 'record_time': datetime.datetime.now()}
            db.secie.insert_one(record)

            # 每五秒采集一次数据
            time.sleep(5)

        except KeyboardInterrupt:  # ctrl+c 停止
            print('Stopped')


if __name__ == '__main__':
    get_info_writedb('192.168.1.7', '123321')
    # snmpv2_get('192.168.168.3', '123321', '1.3.6.1.4.1.2011.6.3.5.1.1.3.0.0.0')



