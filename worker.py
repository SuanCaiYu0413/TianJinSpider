# @Time    : 2018/5/24 20:35
# @Author  : SuanCaiYu
# @File    : worker
# @Software: PyCharm
#
#                  ___====-_  _-====___
#            _--^^^*****//      \\*****^^^--_
#         _-^**********// (    ) \\**********^-_
#        -************//  |\^^/|  \\************-
#      _/************//   (@::@)   \\************\_
#     /*************((     \\//     ))*************\
#    -***************\\    (oo)    //***************-
#   -*****************\\  / VV \  //*****************-
#  -*******************\\/      \//*******************-
# _*/|**********/\******(   /\   )******/\**********|\*_
# |/ |*/\*/\*/\/  \*/\**\  |  |  /**/\*/  \/\*/\*/\*| \|
# `  |/  V  V  `   V  \*\| |  | |/*/  V   '  V  V  \|  '
#    `   `  `      `   / | |  | | \   '      '  '   '
#                     (  | |  | |  )
#                    __\ | |  | | /__
#                   (vvv(VVV)(VVV)vvv)
#                        神兽保佑
#                       代码无BUG!
import time, sys
from queue import Queue
from urllib.parse import quote

from DB import DB
from spider import Crawl
from multiprocessing.managers import BaseManager


class QueueManager(BaseManager):
    pass


QueueManager.register('get_task_queue')

server_addr = '这里填队列管理进程的服务器'
print('Connect to server %s...' % server_addr)

m = QueueManager(address=(server_addr, 12345), authkey=b'abc')

m.connect()

task = m.get_task_queue()
db = DB()

while True:
    try:
        n = task.get(timeout=1)
        print('run task %d...' % n.get('id'))
        crawl = Crawl(
            'http://www.tjfdc.com.cn/Pages/fcdt/fcdtlist.aspx?SelMnu=FCSJ_XMXX&KPZT=&strKPZT=&QY=&XZQH=&strXZQH=&BK=&XMMC=%s' % quote(
                n.get('name'), 'utf-8'))
        try:
            result = crawl.get_project_urls(n.get('name'))
            for item in result:
                db.run_sql(item)
            db.commit()
            db.update(n.get('id'))
        except Exception as e:
            print('丢失项目')
            continue
        time.sleep(1)
    except Exception as e:
        print('task queue is empty.')
        time.sleep(20)
