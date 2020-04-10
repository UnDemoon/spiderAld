# 阿拉丁平台模拟登陆数据爬取工具
**运行方式**
```
	python3 main.py
```

**运用接口**
百度智能云文字识别接口用于识别验证码
[https://ai.baidu.com/](https://ai.baidu.com/)

**运行机制说明**
1.	连接数据库，获取阿拉丁账号；
2.	获取secretKey与验证码图片；
3.	识别验证码删除图片并登陆获取token；
4.	利用token访问接口获取数据；
5.	保存数据到数据库，关闭数据库连接；

**注**
验证码错误（验证码文字）会再进行4次尝试
账号或密码错误只会在进行1次尝试
