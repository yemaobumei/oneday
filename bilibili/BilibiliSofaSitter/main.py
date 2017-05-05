#!/usr/bin/python3
#coding=utf-8

from login import login
#首先进行B站登录,返回发送弹幕姬
client=login()


#建立直播弹幕websocket
import asyncio
from DanmuWebsocket import DanmuWebsocket

danmuji = DanmuWebsocket()

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


