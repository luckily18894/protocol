# -*- coding=utf-8 -*-

from flask import Flask, request
import json
import datetime
import os
import base64

node = Flask(__name__)


# Flask实现RPC,接收POST JSON数据,处理并返回JSON数据
@node.route('/date', methods=['POST'])
def json_date():
    if request.method == 'POST':
        # 获取POST请求中的JSON数据
        dict = request.get_json()
        # print(dict)
        if dict['function'] == 'datetime':  # 如果function为datetime,就返回日期与时间
            return json.dumps({'datetime': str(datetime.datetime.now())})
        elif dict['function'] == 'date':  # 如果function为date,仅返回日期
            return json.dumps({'date': str(datetime.date.today())})


@node.route('/cmd', methods=['POST'])
def json_cmd():
    if request.method == 'POST':
        # 获取POST请求中的JSON数据
        dict = request.get_json()
        cmd_result = os.popen(dict['cmd']).read().encode()
        return json.dumps({'result': base64.b64encode(cmd_result).decode()})


@node.route('/upload/<filename>', methods=['PUT'])
def json_upload(filename):
    if request.method == 'PUT':
        # 获取POST请求中的JSON数据
        dict = request.get_json()
        f = open('upload/recive_{0}'.format(filename), 'wb')
        f.write(base64.b64decode(dict['file_bit'].encode()))
        f.close()
        return json.dumps({'result': 'ok!'})


@node.route('/download/<filename>', methods=['GET'])
def json_download(filename):
    if request.method == 'GET':
        f = open('{0}'.format(filename), 'rb').read()
        base64.b64encode(f).decode()
        return json.dumps({'file_bit': base64.b64encode(f).decode()})


if __name__ == "__main__":
    # 在linux上可以使用'0.0.0.0'
    node.run(host='192.168.1.2', port=80)
