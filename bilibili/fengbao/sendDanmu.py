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
	# {'username':'13126772351','password':'ye06021123','roomid':4416185},
	# {'username':'979365217@qq.com','password':'ye06021123','roomid':2570641},
	# {'username':'13375190907','password':'licca0907','roomid':2570641},
	# {'username':'13390776820','password':'wsglr3636...','roomid':2570641},
	# {'username':'15675178724','password':'zero082570X','roomid':4416185},
	{'username':'15130169870','password':'30169870.','roomid':4416185}
]

cookies_list = []
clients = []
for each in info:		
	LoginClient=Client(each['username'],each['password'])
	cookies,nickname=LoginClient.cookies_login() 
	if not LoginClient.isLogin:
		raise MyError('登陆失败')
	cookies_list.append(cookies)
	clients.append(LoginClient)
while True:
	msg = input('请输入要发送的弹幕内容：')
	for client in clients:
		client.sendDanmu(roomid,msg)