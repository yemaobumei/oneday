#!/usr/bin/python3
#coding=utf-8

import sys
import os
import asyncio
import aiohttp

from DanmuWebsocket import DanmuWebsocket
from api import Client

import requests
import json

#from sql import addUser
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

roomid=[]
for i in range(0,7):
    r=requests.get('http://api.live.bilibili.com/area/liveList?area=all&order=online&page=%s'%(i))
    if r.status_code==200:
        data=json.loads(r.content.decode('utf8'))['data']
        for each_room in data:
            roomid.append(each_room['roomid'])

roomid = list(set(roomid))
print(len(roomid))




#建立直播弹幕websocket,返回发送弹幕姬
danmuji=[]
for each in roomid:
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


