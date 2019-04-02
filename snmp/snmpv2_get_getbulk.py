# -*- coding=utf-8 -*-

from pysnmp.hlapi import *
from pysnmp.entity.rfc3413.oneliner import cmdgen


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
    print(result)
    # 返回的为一个元组,OID与字符串结果
    # return result.split("=")[0].strip(), result.split("=")[1].strip()


def snmpv2_getbulk(ip, community, oid, count=25, port=161):
    cmdGen = cmdgen.CommandGenerator()

    errorIndication, errorStatus, errorindex, varBindTable = cmdGen.bulkCmd(
        cmdgen.CommunityData(community),  # 配置community
        cmdgen.UdpTransportTarget((ip, port)),  # 配置IP地址和端口号
        0, count,  # 0为non-repeaters 和  25为max-repetitions(一个数据包中最多25个条目，和显示无关)
        oid,  # OID
    )

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
        print('%s at %s' % (
            errorStatus.prettyPrint(),
            errorindex and varBinds[int(errorindex) - 1][0] or '?'
        )
              )

    result = []
    # varBindTable是个list，元素的个数可能有好多个。它的元素也是list，这个list里的元素是ObjectType，个数只有1个。
    cal = 1
    for varBindTableRow in varBindTable:
        for item in varBindTableRow:
            result.append((cal, item.prettyPrint().split("=")[0].strip(), item.prettyPrint().split("=")[1].strip()))
            cal += 1
    # print(result)
    return result


if __name__ == '__main__':
    # snmpv2_get('192.168.1.107', '123321', '1.3.6.1.2.1.2.2.1.2')

    # print((snmpv2_getbulk("192.168.1.107", "123321", "1.3.6.1.2.1.2.2.1.5", count=25, port=161)))

    # for a in snmpv2_getbulk("192.168.1.107", "123321", "1.3.6.1.2.1.2.2.1.2", count=25, port=161):
    #     print(a)

    # # 接口带宽
    for a in snmpv2_getbulk("192.168.1.107", "123321", "1.3.6.1.2.1.2.2.1.5", port=161):
        print(a)

    # # 进接口字节数
    # for a in snmpv2_getbulk("192.168.1.107", "123321", "1.3.6.1.2.1.2.2.1.10", port=161):
    #     print(a)

    # # 出接口字节数
    # for a in snmpv2_getbulk("192.168.1.107", "123321", "1.3.6.1.2.1.2.2.1.16", port=161):
    #     print(a)
