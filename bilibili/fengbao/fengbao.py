#!/usr/bin/python3
#coding=utf-8

import os,sys
sys.path.append("../")
#异步操作
import asyncio
import aiohttp

from DanmuWebsocket import DanmuWebsocket
from helper.api import Client,MyError

import requests
import json
import time
from helper import config


#登录B站获取cookies
info = [
	{'username':'13126772351','password':'ye06021123','roomid':1273106},
#	{'username':'979365217@qq.com','password':'ye06021123','roomid':2570641},
#	{'username':'13375190907','password':'licca0907','roomid':2570641},
	{'username':'13390776820','password':'wsglr3636...','roomid':2570641}

]
cookies_list = []
for each in info:		
	LoginClient=Client(each['username'],each['password'])
	cookies,nickname=LoginClient.cookies_login() #<class set (1,2)>
	if not LoginClient.isLogin:
		raise MyError('登陆失败')
	cookies_list.append(cookies)


#获取最新热门直播房间号
room=[]
s = requests.Session()
proxies=config.proxies
s.proxies=proxies
s.keep_alive = False
headers={'Connection':'close'}

for i in range(0,7):
	j=0
	while True:
		j += 1
		if j > 40:
			raise MyError('获取最新直播房间号失败')	
		try:
			r=s.get('http://api.live.bilibili.com/area/liveList?area=all&order=online&page=%s'%(i),timeout=5)
			if r.status_code==200:
				data=r.json()['data']
				for each_room in data:
					room.append(each_room['roomid'])
				break
			else:
				raise MyError("获取直播信息失败第%s次,http错误号:%s"%(j,r.status_code))
		except Exception as e:
			print("fengbao.py:61",e)
			#查询代理ip地址
			#http://www.daxiangdaili.com/api?tid=559329887212274
			#更换代理ip地址
			try:				
				response=requests.get("http://vtp.daxiangdaili.com/ip/?tid=559329887212274&num=1&protocol=http&operator=1&delay=1&filter=on",timeout=5)
				ip=response.text
				if response.status_code == 200:
					proxies['http']=ip
					proxies['https']=ip
					#print(ip)
					f=open('../helper/config.py','w')
					f.write('proxies=%s'%(proxies))
					f.close()
				else:
					raise MyError("代理ip失败,http_code:%s"%(response.status_code))
			except Exception as e:
				print("fengbao.py:78",e)
		finally:
			time.sleep(2)#休息一下，防止访问频率太高

room=list(set(room))
print(len(room))
#room=['2570641']


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


