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

#数据库操作
from sql import addUser

#登录B站获取cookies
username="13126772351"
password="ye06021123"

LoginClient=Client(username,password)
cookies=LoginClient.cookies_login() #<class dic>{}
while not LoginClient.isLogin:
	LoginClient.login()
	if LoginClient.isLogin:
		cookies=LoginClient.cookies_login()
		break

room=[]
for i in range(0,7):
	r=requests.get('http://api.live.bilibili.com/area/liveList?area=all&order=online&page=%s'%(i))
	if r.status_code==200:
		data=json.loads(r.content.decode('utf8'))['data']
		for each_room in data:
			room.append(each_room['roomid'])
			#获取主播信息
			# uid=int(each_room['uid'])
			# uname=each_room['uname']
			# roomid=int(each_room['link'].replace('/',''))
			# realRoomid=int(each_room['roomid'])
			# areaName=each_room['areaName']
			# online=each_room['online']
			#获取主播粉丝数
			# s=requests.get('http://space.bilibili.com/ajax/friend/GetFansList?mid=%s&page=1&_=1494764064486'%(uid))#mid输入uid.
			# data=json.loads(s.content.decode('utf8'))['data']#可能是字典，也可能是"粉丝列表中没有值"
			# fansnum=int(data['results']) if 'results' in data else 0
			#print(i,uname,online)
			#数据库添加用户信息
			# addUser(uid,uname,roomid,realRoomid,fansnum,areaName)
			

room = list(set(room))
print(len(room))




#建立直播弹幕websocket,返回发送弹幕姬
danmuji=[]
for each in room:
	danmuji.append(DanmuWebsocket(cookies=cookies,roomid=each))


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


