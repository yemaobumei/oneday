#!/usr/bin/python3
#coding=utf-8

import sys
import os
import asyncio
import aiohttp


from api import Client



info = [
	{'username':'13126772351','password':'13126772351','roomid':545342},
	{'username':'979365217@qq.com','password':'ye06021123','roomid':545342},
	{'username':'13390776820','password':'wsglr3636...','roomid':545342}
]
tasks = []
for each in info:		
	LoginClient=Client(each['username'],each['password'])
	cookies=LoginClient.cookies_login() #<class dic>{}
	while not LoginClient.isLogin:
		LoginClient.login()
		if LoginClient.isLogin:
			cookies=LoginClient.cookies_login()
			break

	#添加异步任务
	tasks+=[
				LoginClient.sendDanmu(each['roomid'],'选择小米不会有错!'),
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


