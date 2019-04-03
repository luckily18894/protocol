# -*- coding=utf-8 -*-

from difflib import *


def diff_file(file1, file2):
    txt1 = open(file1, 'r').readlines()
    txt2 = open(file2, 'r').readlines()
    result = Differ().compare(txt1, txt2)
    return_result = '\r\n'.join(list(result))
    return return_result


def diff_txt(txt1, txt2):
    txt1_list = txt1.split('\r\n')
    txt2_list = txt2.split('\r\n')
    result = Differ().compare(txt1_list, txt2_list)
    return_result = '\r\n'.join(list(result))
    return return_result


if __name__ == '__main__':
    txt_1 = "\r\nBuilding configuration...\r\n\r\nCurrent configuration : 2406 bytes\r\n!\r\nversion 15.2\r\nservice timestamps debug datetime msec\r\nservice timestamps log datetime msec\r\n!\r\nhostname R1\r\n!\r\nboot-start-marker\r\nboot-end-marker\r\n!\r\n!\r\n!\r\nno aaa new-model\r\n!\r\n!\r\n!\r\n!\r\n!\r\n!\r"
    txt_2 = "\r\nBuilding configur...\r\n\r\nCurrent configuran : 2407 bytes\r\n!\r\nversion 15.2\r\nservice timestamps debug datetime msec\r\nservice timestamps log datetime msec\r\n!\r\nhostname R1\r\n!\r\nboot-start-marker\r\nboot-end-marker\r\n!\r\n!\r\n!\r\nno aaa new-model\r\n!\r\n!\r\n!\r\n!\r\n!\r\n!\r"
    print(diff_txt(txt_1, txt_2))



