# -*- coding=utf-8 -*-

from pysnmp.hlapi import *
from pysnmp.entity.rfc3413.oneliner import cmdgen
from pymongo import *
import datetime


def snmpv2_getbulk(ip, community, oid, count=25, port=161):
    cmdGen = cmdgen.CommandGenerator()

    errorIndication, errorStatus, errorindex, varBindTable = cmdGen.bulkCmd(
        cmdgen.CommunityData(community),  # 配置community
        cmdgen.UdpTransportTarget((ip, port)),  # 配置IP地址和端口号
        0, count,  # 0为non-repeaters 和  25为max-repetitions(一个数据包中最多25个条目，和显示无关)
        oid,)  # OID

    """
    non-repeaters介绍
    the number of objects that are only expected to return a single GETNEXT instance, not multiple instances. Managers frequently request the value of sysUpTime and only want that instance plus a list of other objects.
    max-repetitions介绍
    the number of objects that should be returned for all the repeating OIDs. Agent's must truncate the list to something shorter if it won't fit within the max-message size supported by the command generator or the agent.
    详细介绍
    https://www.webnms.com/snmp/help/snmpapi/snmpv3/snmp_operations/snmp_getbulk.html
    """
    # 错误处理
    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(), errorindex and varBinds[int(errorindex) - 1][0] or '?'))

    result = []
    # varBindTable是个list，元素的个数可能有好多个。它的元素也是list，这个list里的元素是ObjectType，个数只有1个。
    cal = 1
    for varBindTableRow in varBindTable:
        for item in varBindTableRow:
            result.append((cal, item.prettyPrint().split("=")[0].strip(), item.prettyPrint().split("=")[1].strip()))
            cal += 1
    # print(result)
    return result


def get_interface_information_to_db(interface_number):
    # 得到的信息 在真实端口前还包含类似 lo vlanif1，手动忽略，vlanif2 +  排在所有物理口之后
    real_number = interface_number + 4

    # snmpv2_getbulk.....  获取所有端口的带宽、入方向、出方向字节数
    name = snmpv2_getbulk("192.168.1.107", "123321", "1.3.6.1.2.1.2.2.1.2")[real_number][2]
    speed = snmpv2_getbulk('192.168.1.107', '123321', '1.3.6.1.2.1.2.2.1.5')[real_number][2]
    in_bytes = snmpv2_getbulk('192.168.1.107', '123321', '1.3.6.1.2.1.2.2.1.10')[real_number][2]
    out_bytes = snmpv2_getbulk('192.168.1.107', '123321', '1.3.6.1.2.1.2.2.1.16')[real_number][2]

    # 入库
    client = MongoClient('mongodb://luckily18894:luCKi1y18894@192.168.1.110:27017/pythondb')
    db = client['pythondb']
    # db.secie.remove()

    record = {'if_name': name,
              'in_bytes': int(in_bytes),
              'out_bytes': int(out_bytes),
              'speed': int(speed),
              'record_time': datetime.datetime.now()}

    db.secie.insert_one(record)

    # print(record)


if __name__ == '__main__':
    import time

    while True:
        try:
            get_interface_information_to_db(1)
            get_interface_information_to_db(2)
            get_interface_information_to_db(3)
            time.sleep(1)
        except KeyboardInterrupt:
            print('stopped')


