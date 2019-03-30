# -*- coding=utf-8 -*-

import logging
import socketserver
import threading
import re

# LOG_FILE = 'pysyslog.log'
#
# logging.basicConfig(level=logging.INFO,
#                     format='%(message)s',
#                     datefmt='',
#                     filename=LOG_FILE,  # log文件
#                     filemode='a')  # 追加模式


class SyslogUDPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = bytes.decode(self.request[0].strip())  # 读取数据
        # ============可以配置过滤器仅仅读取接口up/down信息===============
        # if re.match('.*changed state to administratively down.*', data):
        #     print( "%s : " % self.client_address[0], str(data))
        # elif re.match('.*changed state to up.*', data):
        #     print( "%s : " % self.client_address[0], str(data))
        # print(str(data))
        print("%s : " % self.client_address[0], str(data))  # 打印syslog信息
        # logging.info(str(data))  # 把信息logging到本地


if __name__ == "__main__":
    # 使用Linux解释器 & WIN解释器
    try:
        HOST, PORT = "0.0.0.0", 514  # 本地地址与端口
        server = socketserver.UDPServer((HOST, PORT), SyslogUDPHandler)  # 绑定本地地址，端口和syslog处理方法
        print("Syslog 服务已启用, 写入日志到文本文件!!!")
        server.serve_forever(poll_interval=0.5)  # 运行服务器，和轮询间隔

    except (IOError, SystemExit):
        raise
    except KeyboardInterrupt:  # 捕获Ctrl+C，打印信息并退出
        print("Crtl+C Pressed. Shutting down.")

