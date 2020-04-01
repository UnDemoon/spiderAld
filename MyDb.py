# -*- coding: utf-8 -*-

#   基础模块
import time
import warnings
import os
import sys
import json

#   mysql相关
import pymysql



warnings.filterwarnings("ignore")


class MyDb(object):
    def __init__(self, dbconfig):
        self.conf = dbconfig        #   配置数组
        self.timer_connet = 0
        self.db = self.connectDb()

    #       链接db
    def connectDb(self):
        self.timer_connet += 1
        try:
            con = pymysql.connect(
                host = self.conf['host'],
                user = self.conf['user'],
                passwd = self.conf['passwd'],
                db = self.conf['db'],
                charset = self.conf['charset']
            )
        except Exception as e:
            #   最大重连次数
            if self.timer_connet >= 5:
                logFile("连接数据库失败")
                sys.exit()
            else:
                #   尝试重连
                sleeptime = self.timer_connet * 60
                time.sleep(sleeptime)
                self.connectMysql(conf)
        return con

    #   查找
    def findFrom(self, table, where, order="", all=False):
        #   读取源数据库表
        cur = self.db.cursor()
        sqlstr = "SELECT * FROM " + table + " WHERE " + where + " " + order
        cur.execute(sqlstr)
        if all:
            res = cur.fetchall()
        else:
            res = cur.fetchone()
        return res

    def saveTo(self, table, data, update_id = None):
        cur = self.db.cursor()
        if update_id:
            str_sql = ""
            for k, v in data.items():
                str_sql += "`%s`=%s, " % (k, v) if v == "NULL"  else "`%s`=\"%s\", " % (k, v)
            sql = "UPDATE %s SET %s WHERE id=\"%s\"" % (table, str_sql.strip().strip(","), update_id)
        else:
            str1 = str2 = ""
            for k, v in data.items():
                str1 += str(k) + ","
                str2 += str(v) + "," if v == "NULL"  else "\"" + str(v) + "\","
            sql = "INSERT INTO %s ( %s ) VALUES (%s)" % (table, str1.strip().strip(","), str2.strip().strip(","))
        try:
            cur.execute(sql)
            self.db.commit()
        except Exception as e:
            #logFile(str(e))
            logFile(sql)

    def closeCon(self):
        cur.close()
        self.db.close()

    #   错误信息
def logFile( msg):
    with open('dblog.log', 'a') as f:
        f.write(str(int(time.time())) +":"+ msg + "\n")
