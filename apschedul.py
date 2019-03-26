# -*- coding=utf-8 -*-

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from datetime import datetime
import logging
from ssh import write_config_md5_to_db

# 记录日志
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='log1.txt',
                    filemode='a')


# 测试函数 # 可以换为import的获取路由器配置并写入数据库的脚本
# def qyt_print(x, y):
#     print('测试答应信息!', x, y)
#     # print(1/0) # 制造错误


# 事件处理函数
def my_listener(event):

    job_id = event.job_id  # 获取job_id

    if event.exception:  # 如果执行出现故障
        debug_message = event.traceback  # 获取debug信息
        print(job_id + '执行出错!')
        print('错误信息如下:')
        print(debug_message)

    else:
        print(job_id + '正常执行!')


scheduler = BlockingScheduler()

# scheduler.add_job  func=所执行的函数，args=[函数的参数 使用列表]，trigger=调度的模式

# cron调度
# cron: 使用同linux下crontab的方式(year=None, month=None, day=None, week=None, day_of_week=None, hour=None, minute=None,\
# second=None, start_date=None, end_date=None, timezone=None)
# hour =19 , minute =23
# hour ='19', minute ='23'
# minute = '*/3' 表示每 5 分钟执行一次
# hour ='19-21', minute= '23' 表示 19:23、 20:23、 21:23 各执行一次任务
scheduler.add_job(func=write_config_md5_to_db, trigger='cron', hour='5-7', minute=37, id='cron调度!测试正常打印!')

# date: 只在某个时间点执行一次run_date(datetime|str)
scheduler.add_job(func=write_config_md5_to_db, trigger='date', run_date=datetime(2019, 3, 27, 6, 38), id='date调度!测试正常打印!')

# interval: 每隔一段时间执行一次weeks=0 | days=0 | hours=0 | minutes=0 | seconds=0, start_date=None, end_date=None, timezone=None
scheduler.add_job(func=write_config_md5_to_db, trigger='interval', minutes=1,
                  start_date=datetime(2019, 3, 27, 6, 40), end_date=datetime(2019, 3, 27, 6, 45), id='interval调度!测试正常打印!')

# 加载事件处理函数
scheduler.add_listener(my_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
# 记录日志
scheduler._logger = logging
# 开始调度
scheduler.start()


if __name__ == '__main__':
    pass
