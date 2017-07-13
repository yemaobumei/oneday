#!/usr/bin/python3  
# -*- coding: utf-8 -*-  


from getTopUp import GetTopUpRoomId
from DanmuClientManager import DanmuClientManager, FengbaoClientManager, getRoomList
import sys
sys.path.append("../")
from helper.api import Client


info = [
#	{'username':'13126772351','password':'ye06021123','roomid':4416185},
	{'username':'979365217@qq.com','password':'ye06021123','roomid':2570641},
#	{'username':'13375190907','password':'licca0907','roomid':2570641},
#	{'username':'13390776820','password':'wsglr3636...','roomid':2570641},
#	{'username':'15675178724','password':'zero082570X','roomid':4416185}
]

if __name__ == '__main__':
	#登录B站获取cookies
	cookieslist = []
	for each in info:
		LoginClient = Client(each['username'],each['password'])
		cookies,nickname = LoginClient.cookies_login()
		cookieslist.append(cookies)
	#获取直播房间号		
	roomList = getRoomList(0,7)
	roomList += [2570641]

	#启动任务管理器
	#cm = DanmuClientManager(roomInfo = roomList)
	cm = FengbaoClientManager(roomInfo = {'roomList':roomList,'cookieslist':cookieslist})
	cm.start()