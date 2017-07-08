#!/usr/bin/python3
#coding=utf-8

import os
import asyncio
import aiohttp

from DanmuWebsocket import DanmuWebsocket

import sys
sys.path.append("../")
from helper.api import Client


#登录B站获取cookies

info = [
	{'username':'13126772351','password':'ye06021123','roomid':4416185},
	{'username':'979365217@qq.com','password':'ye06021123','roomid':4416185},
	{'username':'13390776820','password':'wsglr3636...','roomid':4416185},
	{'username':'13375190907','password':'licca0907','roomid':4416185}
]
tasks = []
for each in info:		
	LoginClient=Client(each['username'],each['password'])
	cookies,nickname=LoginClient.cookies_login() #<class dic>{}
	while not LoginClient.isLogin:
		LoginClient.login()
		if LoginClient.isLogin:
			cookies,nickname=LoginClient.cookies_login()
			break
	#建立直播弹幕websocket,返回发送弹幕姬
	danmuji = DanmuWebsocket(cookies=cookies,roomid=each['roomid'],nickname=nickname)
	#添加异步任务
	tasks+=[
				#danmuji.sendDanmu('小夜猫来看你了'),
				LoginClient.do_sign(),
				danmuji.connectServer(),
				danmuji.HeartbeatLoop()
			]		


loop = asyncio.get_event_loop()
try:
	loop.run_until_complete(asyncio.wait(tasks))
# except KeyboardInterrupt:
	# danmuji.connected = False
	# for task in asyncio.Task.all_tasks():
	#     task.cancel()
	#     loop.run_forever()
	# pass
except Exception as e:
	print(e)
loop.close()


