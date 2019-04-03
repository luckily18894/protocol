# -*- coding=utf-8 -*-

import paramiko
import hashlib
import re
from difflib import *
from pymongo import *
import datetime
import smtplib
import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


def smtp_attachment(mailserver, username, password, From, To, Subj, Main_Body, files=None):
    # 使用SSL加密SMTP发送邮件, 此函数发送的邮件有主题,有正文,还可以发送附件
    Tos = To.split(';')  # 把多个邮件接受者通过';'分开
    Date = email.utils.formatdate()  # 格式化邮件时间
    msg = MIMEMultipart()  # 产生MIME多部分的邮件信息
    msg["Subject"] = Subj  # 主题
    msg["From"] = From  # 发件人
    msg["To"] = To  # 收件人
    msg["Date"] = Date  # 发件日期

    part = MIMEText(Main_Body)
    msg.attach(part)  # 添加正文

    if files:  # 如果存在附件文件
        for file in files:  # 逐个读取文件,并添加到附件
            part = MIMEApplication(open(file, 'rb').read())
            part.add_header('Content-Disposition', 'attachment', filename=file)
            msg.attach(part)

    server = smtplib.SMTP_SSL(mailserver, 465)  # 连接邮件服务器
    server.login(username, password)  # 通过用户名和密码登录邮件服务器
    failed = server.sendmail(From, Tos, msg.as_string())  # 发送邮件
    server.quit()  # 退出会话
    if failed:
        print('Falied recipients:', failed)  # 如果出现故障，打印故障原因！
    else:
        print('邮件已经成功发出！')  # 如果没有故障发生，打印'邮件已经成功发出！'！


def diff_txt(txt1, txt2):
    txt1_list = txt1.split('\r\n')
    txt2_list = txt2.split('\r\n')
    result = Differ().compare(txt1_list, txt2_list)
    return_result = '\r\n'.join(list(result))
    return return_result


def py_ssh(ip, username, password, port=22, cmd='ls'):
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, username=username, port=port, password=password, timeout=5, compress=True)
    stdin, stdout, stderr = ssh.exec_command(cmd)
    x = stdout.read().decode()

    return x


def get_config_md5(ip, username, password):
    run_config_raw = py_ssh(ip, username=username, password=password, cmd='dis cu')
    b = re.findall('.*(sysname.*return).*', run_config_raw, re.S | re.M)
    # re.S是代表 . 可以匹配\n以及 ''   re.M是多行

    # c = re.sub('\r', '', b[0])
    run_config = re.sub('\r\n', '\r\n', b[0])
    # 匹配后输出的结果是列表，里面是匹配中的字符串（单行），其中包含可见的\n，所以就替换回去

    m = hashlib.md5()
    m.update(run_config.encode())
    md5_value = m.hexdigest()

    return run_config, md5_value


def write_config_md5_to_db(device_list, username, password, send_to):
    client = MongoClient('mongodb://luckily18894:luCKi1y18894@192.168.1.110:27017/pythondb')
    db = client['pythondb']
    # db.secie.remove()

    for device in device_list:
        config_and_md5 = get_config_md5(ip=device, username=username, password=password)
        time_now = datetime.datetime.now()

        # 查找数据库中 是否有此设备的配置记录 并作出相应操作
        # 如果没有此设备信息 就写入该条目
        if not db.secie.find_one({'ip': device}):
            record = {'ip': device,
                      'config': config_and_md5[0],
                      'md5': config_and_md5[1],
                      'time': time_now}
            db.secie.insert_one(record)
        else:
            md5_results = db.secie.find_one({'ip': device})['md5']

            # 如果md5值不同 发送邮件通知配置不同之处，并更新该条目
            if config_and_md5[1] != md5_results:
                # 对比不同处
                old = db.secie.find_one({'ip': device})['config']
                new = config_and_md5[0]
                differences = diff_txt(old, new)
                # 发送邮件
                smtp_attachment('smtp.qq.com',
                                '185686792@qq.com',
                                'vzzvmemjknzqbhbj',
                                '185686792@qq.com',
                                send_to,
                                '设备{0}配置改变'.format(device),
                                '系统于{0}检测到配置变化\r\n配置比较如下：\r\n{1}'.format(time_now.strftime('%Y.%m.%d %H:%M:%S'),
                                                                                     differences))
                # 更新条目
                db.secie.update({'ip': device}, {"$set": {'config': config_and_md5[0]}})
                db.secie.update({'ip': device}, {"$set": {'md5': config_and_md5[1]}})
                db.secie.update({'ip': device}, {"$set": {'time': time_now}})
                print('配置已经成功更新！')

            # 如果md5值相同 就掠过
            else:
                pass


if __name__ == '__main__':
    device_list = ['192.168.1.107']
    # username = 'root'
    # password = 'huawei'
    send_to = '185686792@qq.com'

    # print(get_config_md5('192.168.1.107', 'root', 'huawei'))
    write_config_md5_to_db(device_list, 'root', 'huawei', send_to)

# smtp_attachment('smtp.qq.com',
#                 '3348326959@qq.com',
#                 'dmyymagcazklcjie',
#                 '3348326959@qq.com',
#                 '3348326959@qq.com;collinsctk@qytang.com',
#                 '附件测试_主题',
#                 '附件测试_正文',
#                 ['Logo.jpg'])


