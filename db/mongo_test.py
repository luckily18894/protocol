# -*- coding=utf-8 -*-

from pymongo import *
from datetime import datetime
client = MongoClient('mongodb://luckily18894:luCKi1y18894@192.168.1.110:27017/pythondb')

db = client['pythondb']

##########简单查询测试##########
# for obj in db.secie.find():
#     print(obj)

##########写入单条数据##########

# tina = {'name': 'tina', 'department': 'sales', 'age': 35, 'location': 'Beijing'}
#
# #写入单条数据
# db.secie.insert_one(tina)
#
# #查看并打印secie中的所有数据
# for obj in db.secie.find():
#     print(obj)

#########写入时间##############
# config = {'config': 'test', 'record_time': datetime.now()}
# db.secie.insert_one(config)
#
# # config键存在, 时间倒序
# for obj in db.secie.find({'config': {"$exists": True}}).sort('record_time', -1):
#     print(obj)
#
# # 时间的过滤
# start = datetime(2019, 3, 29, 21, 15, 6, 395000)
# end = datetime(2019, 3, 29, 22, 12, 48, 257000)
#
# for obj in db.secie.find({'config': {"$exists": True}, 'record_time': {'$gte': start, '$lt': end}}):
#     print(obj)

#########写入二进制文件##############
# from bson import binary
#
# file_insert = {'filename': 'result1.png', 'binfile': binary.Binary(open('result1.png', 'rb').read())}
# db.secie.insert_one(file_insert)
#
# for obj in db.secie.find({'filename': {"$exists": True}}):
#     print(obj)
##########写入多条数据##########
# # 准备写入的多条数据
# employees = [{'name': 'collinsctk', 'department': 'security', 'age': 39, 'location': 'Beijing', 'skill': ['cisco', 'python', 'hacker']},
#              {'name': 'ender', 'department': 'rs', 'age': 35, 'location': 'Shanghai', 'interest': 'basketball'},
#              {'name': 'heymo', 'department': 'dc', 'age': 35, 'location': 'Beijing', 'course': ['nexus', 'ucs', 'storage']}
#              ]
# #逐个单条写入
# for employee in employees:
#     db.secie.insert_one(employee)
#
# #一次性写入多个(写入一个列表)
# db.secie.insert_many(employees)
#
# #查看并打印secie中的所有数据
# for obj in db.secie.find():
#     print(obj)

##########查找单条数据##########
# print(db.secie.find_one({'name': 'collinsctk'}))
#
# print(db.secie.find_one({'age': {'$gt': 34}}))

##########查找多条数据##########
# for x in db.secie.find({'location': 'Beijing'}):
#     print(x)

##########查找多条数据(多条件 and关系)##########
# for x in db.secie.find({'age': {'$gt': 34}, 'location': 'Beijing'}):
#     print(x)

##########查找多条数据(多条件 or关系)##########
# for x in db.secie.find({'$or': [{'age': {'$gt': 34}}, {'location': 'Shanghai'}]}):
#     print(x)

##########查找多条数据(正序与倒序)##########
# for x in db.secie.find({'$or': [{'age': {'$gt': 34}}, {'location': 'Shanghai'}]}).sort('age', ASCENDING):
#     print(x)
#
# for x in db.secie.find({'$or': [{'age': {'$gt': 34}}, {'location': 'Shanghai'}]}).sort('age', DESCENDING):
#     print(x)
#     # 只答应特定字段
#     print(x.get('name'))
#     print(x.get('course'))

##########更新数据##########
# db.secie.update({'name': 'collinsctk'}, {"$set": {'name': "QINKE"}})
#
# for obj in db.secie.find():
#     print(obj)

##########更新多条数据##########
# db.secie.update({'location': 'Beijing'}, {"$set": {'location': "BJ"}})  # 默认只更新一条
#
# for obj in db.secie.find():
#     print(obj)
#
# db.secie.update({'location': 'Beijing'}, {"$set": {'location': "BJ"}}, multi=True)
#
# for obj in db.secie.find():
#     print(obj)

##########删除数据##########
# db.secie.remove({'location': 'BJ'})
#
# for obj in db.secie.find():
#     print(obj)

##########删除全部数据##########
db.secie.remove()


if __name__ == '__main__':
    pass


