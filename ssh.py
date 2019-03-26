# -*- coding=utf-8 -*-

import paramiko
import hashlib
import re
import sqlite3


device_list = ['192.168.1.106']
username = 'root'
password = 'huawei'


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
    run_config = re.sub('\n', '\n', b[0])
    # 匹配后输出的结果是列表，里面是匹配中的字符串（单行），其中包含可见的\n，所以就替换回去

    m = hashlib.md5()
    m.update(run_config.encode())
    md5_value = m.hexdigest()

    return run_config, md5_value


def write_config_md5_to_db():
    conn = sqlite3.connect('configmd5.sqlite')
    cursor = conn.cursor()

    for device in device_list:
        config_and_md5 = get_config_md5(ip=device, username=username, password=password)

        cursor.execute("select md5 from config_md5 where ip = ?", (device,))
        md5_results = cursor.fetchall()

        if not md5_results:
            cursor.execute("insert into config_md5 values('%s', '%s', '%s')" % (device, config_and_md5[0], config_and_md5[1]))
        #     如果没有此md5值 就写入这条目
        else:
            if config_and_md5[1] != md5_results:
                cursor.execute("update config_md5 set config = ?, md5 = ? where ip = ?", (config_and_md5[0], config_and_md5[1], device))
            #     如果md5值不同 就更新该条目
            else:
                pass
    #         如果md5值相同 就掠过

    cursor.execute("select * from config_md5")
    all_result = cursor.fetchall()

    for x in all_result:
        print(x[0], x[2])

    conn.commit()


if __name__ == '__main__':
    # print(get_config_md5('192.168.157.3', 'root', 'huawei')[1])
    write_config_md5_to_db()

