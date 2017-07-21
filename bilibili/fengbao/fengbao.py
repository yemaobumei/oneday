#!/usr/bin/python3
#coding=utf-8

import os,sys
sys.path.append("../")
#异步操作
import asyncio

from DanmuWebsocket import DanmuWebsocket
from helper.api import Client

import room
from getTopUp import GetTopUpRoomId

loop = asyncio.get_event_loop()
#登录B站获取cookies
info = [
#	{'username':'13126772351','password':'ye06021123','roomid':4416185},
	{'username':'979365217@qq.com','password':'ye06021123','roomid':2570641},
#	{'username':'13375190907','password':'licca0907','roomid':2570641},
#	{'username':'13390776820','password':'wsglr3636...','roomid':2570641},
#	{'username':'15675178724','password':'zero082570X','roomid':4416185},
#	{'username':'15130169870','password':'30169870.','roomid':4416185}
]

cookies_list = []
for each in info:		
	LoginClient=Client(each['username'],each['password'])
	cookies,nickname=LoginClient.cookies_login() #<class set (1,2)>
	if not LoginClient.isLogin:
		raise MyError('登陆失败')
	cookies_list.append(cookies)


#获取最新热门直播房间号
try:
	room=room.room
	if len(room) == 0:
		raise MyError("最新热门房间号为空!")
except Exception as e:
	room=GetTopUpRoomId(0,7).start()
print(len(room))

# room +=['2570641']


#建立直播弹幕websocket,返回发送弹幕姬
danmuji=[]
for each in room:
	danmuji.append(DanmuWebsocket(loop=loop,cookies_list=cookies_list,roomid=each))


#执行异步任务
tasks = []
for each in danmuji:
	tasks.append(each.connectServer())
	tasks.append(each.HeartbeatLoop())



try:
	loop.run_until_complete(asyncio.wait(tasks))
except KeyboardInterrupt:
	print("手动关闭")
finally:
	# print(">> Cancelling tasks now")
	for task in asyncio.Task.all_tasks():
	    task.cancel()
	loop.run_until_complete(asyncio.sleep(1))
	print(">> Done cancelling tasks")
	loop.close()



