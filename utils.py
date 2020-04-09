#   工具方法集合
import hashlib
import time
import datetime
import requests
import os
from aippythonsdk.aip import AipOcr

#   md5 code 方法
def md5Code(len=32):
    seed = str(time.time()).encode(encoding='utf-8')
    m = hashlib.md5()
    m.update(seed)
    code = m.hexdigest()
    return code[:len]

#   当前路径
def curPath():
    path = os.path.abspath(os.path.dirname(__file__))
    return path

#   图片下载方法
def downloadImgByUrl(imgurl, savepath = "/temp/", name=None):
    r = requests.get(imgurl,stream=True)
    if not name:
        name = md5Code() + ".jpg"
    filepath = curPath() + savepath + name
    with open(filepath, 'wb') as fd:
        for chunk in r.iter_content():
            fd.write(chunk)
    return filepath

#   删除文件
def delFile(path):
    try:
        os.remove(path)
    except Exception as e:
        pass

#       读取图片文件
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

#       百度api获取验证码
def imgOrcByBaidu(imgpath):
    APP_ID = "19197890"
    API_KEY = "ZE8bgPbxLXYHSwyjrHgF7VkM"
    SECRET_KEY = "NYHVwVBjGX0IIFADYolOpHcUQTGqDEC3"
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    image = get_file_content(imgpath)
    res = client.basicAccurate(image)
    if int(res["words_result_num"]) > 0:
        str = res['words_result'][0]['words']
        str = "".join(filter(lambda s:s.isalnum(), list(str)))
    else:
        str = None
    return str

    #   错误信息
def logFile(type, msg):
    with open('ErrorLog.log', 'a') as f:
        time = datetime.datetime.now()
        f.write("%s:%s-%s\n" % (type, msg, time) )
