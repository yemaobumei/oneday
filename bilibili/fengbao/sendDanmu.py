import os,sys
sys.path.append("../")
from helper.api import Client

#登录B站获取cookies

username="13126772351"#"979365217@qq.com"
password="ye06021123"
roomid=input("输入房间号:")

LoginClient=Client(username,password)
cookies,nickname=LoginClient.cookies_login()
while True:
	msg=input("输入发送弹幕内容:")
	LoginClient.sendDanmu(roomid,msg)