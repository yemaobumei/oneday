#!/usr/bin/python3
#coding=utf-8

import sys
import os
#异步操作
import asyncio
import aiohttp

from DanmuWebsocket import DanmuWebsocket
from api import Client

import requests
import json
import time
import config


#登录B站获取cookies
info = [
	{'username':'13126772351','password':'ye06021123','roomid':1273106},
	{'username':'979365217@qq.com','password':'ye06021123','roomid':2570641},
	{'username':'13375190907','password':'licca0907','roomid':2570641},
	{'username':'13390776820','password':'wsglr3636...','roomid':2570641}

]
cookies_list = []
for each in info:		
	LoginClient=Client(each['username'],each['password'])
	cookies,nickname=LoginClient.cookies_login() #<class dic>{}
	while not LoginClient.isLogin:
		LoginClient.login()
		if LoginClient.isLogin:
			cookies,nickname=LoginClient.cookies_login()
			break
	cookies_list.append(cookies)


room=[]
s = requests.Session()
s.keep_alive = False
headers={'Connection':'close'}
proxies=config.proxies

for i in range(4,6):
	while True:
		try:	
			r=s.get('http://api.live.bilibili.com/area/liveList?area=all&order=online&page=%s'%(i),timeout=5,proxies=proxies)
			if r.status_code==200:
				data=r.json()['data']
				for each_room in data:
					room.append(each_room['roomid'])
				break
			else:
				print(r.status_code)
		except Exception as e:
			print(e)

		time.sleep(5)
		#查询代理ip地址
		#http://www.daxiangdaili.com/api?tid=559329887212274
		response=requests.get("http://vtp.daxiangdaili.com/ip/?tid=559329887212274&num=1&protocol=http&operator=1&delay=1&filter=on")
		ip=response.text
		proxies['http']=ip
		print(ip)
		f=open('./config.py','w')
		f.write('proxies=%s'%(proxies))
		f.close()


print(len(room))


#建立直播弹幕websocket,返回发送弹幕姬
danmuji=[]
for each in room:
	danmuji.append(DanmuWebsocket(cookies_list=cookies_list,roomid=each))


#执行异步任务
tasks = []
for each in danmuji:
	tasks.append(each.connectServer())
	tasks.append(each.HeartbeatLoop())


loop = asyncio.get_event_loop()
try:
	loop.run_until_complete(asyncio.wait(tasks))
except KeyboardInterrupt:
	pass

loop.close()


