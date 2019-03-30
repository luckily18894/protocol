# -*- coding=utf-8 -*-

import logging
import socketserver
import threading
import re
from dateutil import parser
import os
import sqlite3
from datetime import datetime

# facility与ID的对应关系的字典
facility_dict = {0: 'KERN',
                 1: 'USER',
                 2: 'MAIL',
                 3: 'DAEMON',
                 4: 'AUTH',
                 5: 'SYSLOG',
                 6: 'LPR',
                 7: 'NEWS',
                 8: 'UUCP',
                 9: 'CRON',
                 10: 'AUTHPRIV',
                 11: 'FTP',
                 16: 'LOCAL0',
                 17: 'LOCAL1',
                 18: 'LOCAL2',
                 19: 'LOCAL3',
                 20: 'LOCAL4',
                 21: 'LOCAL5',
                 22: 'LOCAL6',
                 23: 'LOCAL7'}

# severity_level与ID的对应关系的字典
severity_level_dict = {0: 'EMERG',
                       1: 'ALERT',
                       2: 'CRIT',
                       3: 'ERR',
                       4: 'WARNING',
                       5: 'NOTICE',
                       6: 'INFO',
                       7: 'DEBUG'}


class SyslogUDPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = bytes.decode(self.request[0].strip())  # 读取数据
        # print(data)
        syslog_info_dict = {'device_ip': self.client_address[0]}
        try:
            syslog_info = re.match('<(\d*)>(.*) Huawei %%(\w*)/(\d)/.*\[(\d+)]:.*:(.*)\..*(Pro.*)\)', str(data)).groups()
            # print(syslog_info[0]) 提取为整数 例如 185
            # 185 二进制为 1011 1001
            # 前5位为facility  >> 3 获取前5位
            # 后3位为severity_level  & 0b111 获取后3位
            syslog_info_dict['facility'] = (int(syslog_info[0]) >> 3)
            syslog_info_dict['facility_name'] = facility_dict[int(syslog_info[0]) >> 3]
            syslog_info_dict['time'] = parser.parse(syslog_info[1])
            syslog_info_dict['logid'] = int(syslog_info[4])
            syslog_info_dict['log_source'] = syslog_info[2]
            syslog_info_dict['severity_level'] = int(syslog_info[3])
            syslog_info_dict['severity_level_name'] = severity_level_dict[int(syslog_info[3])]
            syslog_info_dict['description'] = syslog_info[5]
            syslog_info_dict['text'] = syslog_info[6]
        # except AttributeError:
            # syslog_info = re.match('^<(\d*)>(\d*): \*(.*): (\w+): (.*)', str(data)).groups()
            # print(syslog_info[0])
            # syslog_info_dict['facility'] = (int(syslog_info[0]) >> 3)
            # syslog_info_dict['facility_name'] = facility_dict[int(syslog_info[0]) >> 3]
            # syslog_info_dict['logid'] = int(syslog_info[1])
            # syslog_info_dict['time'] = parser.parse(syslog_info[2])
            # syslog_info_dict['log_source'] = syslog_info[3]

            # 如果在文本部分解析不了severity_level, 切换到syslog_info[0]去获取
            # 185 二进制为 1011 1001
            # 前5位为facility  >> 3 获取前5位
            # 后3位为severity_level  & 0b111 获取后3位
            # syslog_info_dict['severity_level'] = (int(syslog_info[0]) & 0b111)
            # syslog_info_dict['severity_level_name'] = severity_level_dict[(int(syslog_info[0]) & 0b111)]
            # syslog_info_dict['description'] = 'N/A'
            # syslog_info_dict['text'] = syslog_info[4]

            # print(syslog_info_dict)

            conn = sqlite3.connect(gl_dbname)
            cursor = conn.cursor()
            cursor.execute("insert into syslogdb (time, device_ip, facility, facility_name, severity_level, \
                                                  severity_level_name, logid, log_source, description, text) "
                           "values ('%s', '%s', %d, '%s', %d, '%s', %d, '%s', '%s', '%s')" % (syslog_info_dict['time'].strftime("%Y-%m-%d %H:%M:%S"),
                                                                                    syslog_info_dict['device_ip'],
                                                                                    syslog_info_dict['facility'],
                                                                                    syslog_info_dict['facility_name'],
                                                                                    syslog_info_dict['severity_level'],
                                                                                    syslog_info_dict['severity_level_name'],
                                                                                    syslog_info_dict['logid'],
                                                                                    syslog_info_dict['log_source'],
                                                                                    syslog_info_dict['description'],
                                                                                    syslog_info_dict['text']))
            conn.commit()

            address_status = re.match('.*NeighborAddress=(.*), NeighborEvent.*NeighborCurrentState=(\w+)', syslog_info[6]).groups()
            print(syslog_info[2], 'NeighborAddress', address_status[0], 'status', address_status[1])
        except:
            # 总有些乱七八糟的log，看不上 直接干掉
            print('got one exception')


if __name__ == "__main__":
    # 使用Linux解释器 & WIN解释器
    global gl_dbname
    gl_dbname = 'syslog.sqlite'
    # 若数据库存在就先删除
    if os.path.exists(gl_dbname):
        os.remove(gl_dbname)
    # 连接数据库
    conn = sqlite3.connect(gl_dbname)
    cursor = conn.cursor()
    # 创建数据库

    cursor.execute("create table syslogdb(id INTEGER PRIMARY KEY AUTOINCREMENT,\
                                         time varchar(64), \
                                         device_ip varchar(32),\
                                         facility int,\
                                         facility_name varchar(32),\
                                         severity_level int,\
                                         severity_level_name varchar(32),\
                                         logid int,\
                                         log_source varchar(32), \
                                         description varchar(128), \
                                         text varchar(1024)\
                                         )")
    conn.commit()
    try:
        HOST, PORT = "0.0.0.0", 514  # 本地地址与端口
        server = socketserver.UDPServer((HOST, PORT), SyslogUDPHandler)  # 绑定本地地址，端口和syslog处理方法
        print("Syslog 服务已启用, 写入日志到数据库!!!")
        server.serve_forever(poll_interval=0.5)  # 运行服务器，和轮询间隔

    except (IOError, SystemExit):
        raise
    except KeyboardInterrupt:  # 捕获Ctrl+C，打印信息并退出
        print("Crtl+C Pressed. Shutting down.")
    finally:
        conn.commit()


