# -*- coding=utf-8 -*-

import sqlite3


conn = sqlite3.connect('configmd5.sqlite')
cursor = conn.cursor()
cursor.execute("create table config_md5 (ip varchar(40), config varchar(99999), md5 varchar(999))")


if __name__ == '__main__':
    pass


