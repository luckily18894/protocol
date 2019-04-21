# -*- coding=utf-8 -*-

import requests
import base64


# q1
def datetime_date():
    r = requests.post('HTTp://192.168.1.2/date', json={'function': 'datetime'})
    print(r.json())

    r = requests.post('HTTp://192.168.1.2/date', json={'function': 'date'})
    print(r.json())


# q2
def rpc_cmd():
    r = requests.post('HTTp://192.168.1.2/cmd', json={'cmd': 'ipconfig'})
    print(base64.b64decode(r.json().get('result')).decode('utf-8'))


# q3
def upload_download():
    upload_name = 'upload.png'
    file_bit = base64.b64encode(open(upload_name, 'rb').read()).decode()
    r = requests.put('HTTp://192.168.1.2/upload/{0}'.format(upload_name), json={'file_bit': file_bit})
    print(r.json())

    download_name = 'download.png'
    down_file = 'upload.png'
    r = requests.get('HTTp://192.168.1.2/download/{0}'.format(down_file))
    download_file_bit = base64.b64decode(r.json().get('file_bit').encode())
    f = open(download_name, 'wb')
    f.write(download_file_bit)
    f.close()
    print('{0}文件下载成功'.format(download_name))


if __name__ == '__main__':
    print('任务1：')
    datetime_date()
    print('任务2：')
    rpc_cmd()
    print('任务3：')
    upload_download()

