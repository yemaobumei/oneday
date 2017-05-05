#!/usr/bin/python3
#coding=utf-8
import asyncio
from DanmuWebsocket import DanmuWebsocket

#首先进行B站登录,建立直播弹幕websocket,返回发送弹幕姬
danmuji = DanmuWebsocket()
danmuji.cookies_login()
print(danmuji.isLogin)
danmuji.sendDanmu('lala')


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


