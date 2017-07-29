import os,sys
sys.path.append("../")
from helper.api import Client,MyError

# #登录B站获取cookies

# username="13126772351"#"979365217@qq.com"
# password="ye06021123"
# roomid=input("输入房间号:")

# LoginClient=Client(username,password)
# cookies,nickname=LoginClient.cookies_login()
# while True:
# 	msg=input("输入发送弹幕内容:")
# 	LoginClient.sendDanmu(roomid,msg)


###批量发送弹幕--------------------------------------------
roomid=input("输入房间号:")
#登录B站获取cookies
info = [
	{'username':'13126772351'},
	{'username':'979365217@qq.com'},
	{'username':'13375190907'},
	{'username':'13390776820'},
	{'username':'15675178724'},
	{'username':'15130169870'},
	{'username':'1723506002@qq.com'},
]

cookies_list = []
clients = []
for each in info:		
	LoginClient=Client(each['username'])
	cookies,nickname=LoginClient.cookies_login() 
	if not LoginClient.isLogin:
		raise MyError('登陆失败')
	cookies_list.append(cookies)
	clients.append(LoginClient)
while True:
	msg = input('请输入要发送的弹幕内容：')
	for client in clients:
		client.sendDanmu(roomid,msg)