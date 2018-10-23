# @Time    : 2018/5/25 10:28
# @Author  : SuanCaiYu
# @File    : DB
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
import pymysql


class DB():
    def __init__(self):
        self.DBCONFIG = {
            'host': '',
            'port': 3306,
            'user': '',
            'password': '',
            'db': "Test1",
            'charset': 'utf8',
            'cursorclass': pymysql.cursors.DictCursor
        }
        self.conn = pymysql.connect(**self.DBCONFIG)
        self.cur = self.conn.cursor()
        self.sql = "insert tjfdc(projectcaption,region,blockcaption,blocknum,periodcaption,opentime,blcok_houseprice,blcok_otherprice,selling_blocks,project_address,developers,cell_num,roomcaption,totalfloor,buildarea,publicarea,roomuseage,buildingstructure,locationfloor,innerarea,roomtype,orientation,unitprice,room_link) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    def run_sql(self, result):
        try:
            self.conn.ping()
        except Exception as e:
            self.conn = pymysql.connect(**self.DBCONFIG)
            self.cur = self.conn.cursor()
        self.do_insert(self.cur, result)

    def update(self, id):
        try:
            self.conn.ping()
        except Exception as e:
            self.conn = pymysql.connect(**self.DBCONFIG)
            self.cur = self.conn.cursor()
        self.cur.execute('update `tjfdc_project` set `status`=1 where `id`=%d' % id)
        self.conn.commit()

    def do_insert(self, cursor, item):
        cursor.execute(
            self.sql, (item.get('projectcaption'), item.get('region'), item.get('blockcaption'), item.get('blocknum'),
                       item.get('periodcaption'), item.get('opentime'), item.get('blcok_houseprice'),
                       item.get('blcok_otherprice'), item.get('selling_blocks'), item.get('project_address'),
                       item.get('developers'), item.get('cell_num'), item.get('roomcaption'), item.get('totalfloor'),
                       item.get('buildarea'), item.get('publicarea'), item.get('roomuseage'),
                       item.get('buildingstructure'),
                       item.get('locationfloor'), item.get('innerarea'), item.get('roomtype'), item.get('orientation'),
                       item.get('unitprice'), item.get('room_link')))

    def commit(self):
        self.conn.commit()
        self.cur.close()
        self.cur = self.conn.cursor()

    def close(self):
        self.conn.close()
