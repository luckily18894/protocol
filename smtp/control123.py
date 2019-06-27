# -*- coding=utf-8 -*-

from smtp.pop_recive_mail_per_min import recive_mail, decode_subject_base64
from smtp.send_mail import smtp_attachment
import time
import re
import os

res = {}
while True:
    try:
        # 取得最近一封邮件的内容，做成字典
        for x in recive_mail('pop.qq.com', '185686792@qq.com', 'vzzvmemjknzqbhbj', -8, save_file=False,
                             delete_email=False):
            for key, value in x.items():
                res[key] = value

        # 如果标题是一条指令，就执行
        if re.match('cmd:(.*)', res['Subject']) == 'pwd':
            a = os.popen('pwd').read()
            # 在取得的结果里包含\n  替换掉
            # a = re.sub('\n', '', os.popen('pwd').read())
            # 将执行的结果回复给对方
            smtp_attachment('smtp.qq.com',
                            '185686792@qq.com',
                            'vzzvmemjknzqbhbj',
                            '185686792@qq.com',
                            res['From'],
                            'cmd execute result',
                            a)
        # 时间间隔30s
        time.sleep(30)

    except KeyboardInterrupt:
        print('stopped')




