#
import json
import time
import sys
#
from SpiderAld import SpiderAld
from MyDb import MyDb

#   数据过滤
def dataFiler(d):
    d = d.strip("-")
    d = str(d)
    d = d.replace(",", "");
    if len(d) <= 0:
        d = "NULL"
    return d


#数据保存到数据库
def saveResToDb(resRequests):
    with open("./dbconfig.json", encoding='utf-8') as f:
        config = json.load(f)
        db = MyDb(config)
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
        db.closeCon()


if __name__ == '__main__':
    aldacount, aldpwd = sys.argv[1], sys.argv[2]
    spider = SpiderAld( (aldacount, aldpwd) )
    res =spider.getData()
    saveResToDb(res)
