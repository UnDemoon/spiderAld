#   爬取数据模块
import requests
#   工具方法集合
from utils import *
# from ImgOrc import ImgOrc
#   自定义模块
from MyDb import MyDb
#   忽略警告
import warnings
warnings.filterwarnings("ignore")

class SpiderAld(object):
    """爬取阿拉丁数据"""
    def __init__(self, config):
        self.interface = {      # 接口地址
                            "getcode" :  "https://betaapi.aldwx.com/m/Login_reg/Login/addCode",
                            "sginin"  :  "https://betaapi.aldwx.com/Main/action/Login_reg/Login/login",
                            "getdata" : "https://gameapi.aldwx.com//upgrade/Main/action/Applet/Applet/applet_homepage",
                         }
        self.headers = {         # 消息头数据
                        "access-control-allow-credentials" : "true",
                        "access-control-allow-headers" : "Origin, X-Requested-With, Content-Type, Accept",
                        "access-control-allow-methods" : "GET, POST, OPTIONS",
                        "access-control-allow-origin" : "*",
                        "access-control-max-age" : "1728000",
                        "content-encoding" : "gzip",
                        "content-type" : "application/x-www-form-urlencoded",
                        "date" : "Sat, 28 Mar 2020 03:41:37 GMT",
                        "server" : "nginx",
                        "status" : "200",
                        "vary" : "Accept-Encoding",
                        "x-powered-by" : "PHP/7.1.18"
                        }
        self.token = None
        self.aldaccount = {
                    "phone" : config[0],
                    "password" : config[1]
                }
        self.secretKey = None
        self.maxTry = 5
        self.run()
    #   主运行程序
    def run(self):
        while not self.token and self.maxTry > 0:
            self.maxTry -= 1
            sk, code = self.getCode()
            self.getToken(sk, code)

    #   获取验证码
    def getCode(self):
        secretKey = md5Code(24)
        code = None
        formData = {
                    "secretKey" : secretKey
                    }
        for i in range(0, 5):
            res_requests = requests.post(self.interface["getcode"], formData, headers=self.headers, verify=False)
            res = res_requests.json()
            if res["code"] == 200:
                imgpath = downloadImgByUrl("https://betaapi.aldwx.com" + res["url"])
                code = imgOrcByBaidu(imgpath)
                delFile(imgpath)
                break
            else:
                continue
        return (secretKey, code)

    #           登陆获取token
    def getToken(self, secretKey, code):
        formData = {
                        "phone" : self.aldaccount["phone"],
                        "password" : self.aldaccount["password"],
                        "secretKey" : secretKey,
                        "code" : code
        }
        res_requests = requests.post(self.interface["sginin"], formData, headers=self.headers, verify=False)
        res  = res_requests.json()
        if res["code"] == 200:
            self.token = res["data"]["token"]
        else:
            logFile("requests", res, formData)
            if res["code"] == 202:
                self.maxTry -= 3     #   202错误说明是账号或密码错误，再试一次跳过

    #      获取数据
    def getData(self):
        formData = {
                    "token" : self.token
        }
        res_requests = requests.post(self.interface["getdata"], formData, headers=self.headers, verify=False)
        res = res_requests.json()
        return res
