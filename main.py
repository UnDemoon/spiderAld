#
import json
import time
import sys
#
from SpiderAld import SpiderAld
from MyDb import MyDb

#   工具集合
from utils import *

db = None
#   数据过滤
def dataFiler(d):
    d = d.strip("-")
    d = str(d)
    d = d.replace(",", "");
    if len(d) <= 0:
        d = "NULL"
    return d

#   连接数据库
def dbConnect():
    configfile = curPath() + "/dbconfig.json"
    with open(configfile, encoding='utf-8') as f:
        config = json.load(f)
        global db
        db = MyDb(config)

#数据保存到数据库
def saveResToDb(resRequests):
        global db
        data = resRequests["data"]
        insert = {}
        for item in data:
            for day in item["countList"]:
                insert["app_key"] = item["app_key"]
                insert["app_name"] = item["app_name"]
                insert["platform"] = item["platform"]
                insert["day"] = day["day"]
                insert["new_comer_count"] = dataFiler(day["new_comer_count"])
                insert["visitor_count"] = dataFiler(day["visitor_count"])
                insert["open_count"] = dataFiler(day["open_count"])
                insert["total_page_count"] = dataFiler(day["total_page_count"])
                insert["secondary_avg_stay_time"] = dataFiler(day["secondary_avg_stay_time"])
                insert["bounce_rate"] = dataFiler(day["bounce_rate"])
                insert["total_visitor_count"] = dataFiler(day["total_visitor_count"])
                insert["create_at"] = int(time.time())
                insert["update_at"] = int(time.time())

                where_str = "app_key='%s' AND day='%s' " % (insert["app_key"], insert["day"])
                findone = db.findFrom("wx_ald_app_data", where_str)
                if findone:
                    del insert["create_at"]
                    db.saveTo("wx_ald_app_data", insert, findone[0])
                else:
                    db.saveTo("wx_ald_app_data", insert)

#       读取阿拉丁账号
def loadAccFromDb():
    global db
    where_str = "item_name='%s' AND is_deleted='%s' " % ('aldAccount', '0')
    orderby = ""
    accounts = db.findFrom("global_config", where_str, orderby, True)
    return list(map(lambda item:( item[2].split(';')[0], item[2].split(';')[1] ), accounts))    #   过滤无效数据并切割字符串打包

if __name__ == '__main__':
    dbConnect() #   连接数据库 db用作全局变量
    if db:
        accs = loadAccFromDb()
        for item in accs:
        # for (acc, pwd) in variable:
            # spider = SpiderAld( (aldacount, aldpwd) )
            spider = SpiderAld(item)
            res =spider.getData()
            saveResToDb(res)
        db.closeCon()
