#!/usr/bin/python3
#coding=utf-8
import asyncio
import sys
from DanmuWebsocket import DanmuWebsocket

#首先进行B站登录,建立直播弹幕websocket,返回发送弹幕姬
danmuji = DanmuWebsocket()
if not danmuji.cookies_login():
	print('请手动登录')
	sys.exit()
print(danmuji.isLogin)
danmuji.sendDanmu('小夜猫来看你了')


tasks = [
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


