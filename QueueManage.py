# @Time    : 2018/5/24 20:10
# @Author  : SuanCaiYu
# @File    : QueueManage
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
import random, time
import pymysql
from queue import Queue
from multiprocessing.managers import BaseManager

task_queue = Queue()


class QueueManager(BaseManager):
    pass


def get_projects():
    db_conf = {
        'host': '',
        'port': 1203,
        'user': '',
        'password': '',
        'db': "Test1",
        'charset': 'utf8',
        'cursorclass': pymysql.cursors.DictCursor
    }
    conn = pymysql.connect(**db_conf)
    cur = conn.cursor()
    cur.execute('select `id`,`projectcaption` from `tjfdc_project` where `status`=0')
    result = cur.fetchall()
    cur.close()
    conn.close()
    return result


QueueManager.register('get_task_queue', callable=lambda: task_queue)
manager = QueueManager(address=('0.0.0.0', 12345), authkey=b'abc')
manager.start()
task = manager.get_task_queue()

while True:
    if task.empty():
        result = get_projects()
        if len(result) <= 0:
            break
        for x in result:
            task.put({'id': x.get('id'), 'name': x.get('projectcaption')})
        print('加载完成')
    time.sleep(5)
manager.shutdown()
