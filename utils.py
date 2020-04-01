#   工具方法集合
import hashlib
import time
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

#   图片下载方法
def downloadImgByUrl(imgurl, savepath = "./temp/", name=None):
    r = requests.get(imgurl,stream=True)
    if not name:
        name = md5Code() + ".jpg"
    filepath = savepath + name
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
    str = res['words_result'][0]['words']
    str = "".join(filter(lambda s:s.isalnum(), list(str)))
    return str
