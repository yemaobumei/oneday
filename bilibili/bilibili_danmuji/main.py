#!/usr/bin/python3
#coding=utf-8

import sys
import os
import asyncio
import aiohttp

from DanmuWebsocket import DanmuWebsocket
from api import Client


#登录B站获取cookies
username="979365217@qq.com"
password="ye06021123"
LoginClient=Client()
cookies=LoginClient.cookies_login()
while not LoginClient.isLogin:
	LoginClient.login(username,password)
	if LoginClient.isLogin:
		cookies=LoginClient.cookies_login()
		break

#建立直播弹幕websocket,返回发送弹幕姬
danmuji = DanmuWebsocket(cookies=cookies)


#执行异步任务
tasks = [

			danmuji.sendDanmu('小夜猫来看你了'),
            danmuji.connectServer(),
            danmuji.HeartbeatLoop()
        ]
loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(asyncio.wait(tasks))
except KeyboardInterrupt:
    danmuji.connected = False
    for task in asyncio.Task.all_tasks():
        task.cancel()
    loop.run_forever()

loop.close()


