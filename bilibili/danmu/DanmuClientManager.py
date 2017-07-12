#!/usr/bin/python3  
# -*- coding: utf-8 -*-  

import asyncio
import concurrent.futures
from getTopUp import GetTopUpRoomId
from Bilibili import BilibiliDanmuClient
import room

async def testMemory():
	import os
	import psutil
	# 测试内存占用
	while True:
		process = psutil.Process(os.getpid())
		print(os.getpid(), '占用',
			str(process.memory_info().rss / 1024 / 1024))
		await asyncio.sleep(10)

class DanmuClientManger():
	def __init__(self, loop = None, executor = None, page = [0,7]):
		#私有一个事件循环控制器
		self.loop = loop or asyncio.get_event_loop()
		#私有一个cpu占用型任务的线程池
		self.executor = executor or concurrent.futures.ThreadPoolExecutor(max_workers=100,) 
		
		# 得到需要连接的直播房间列表
		self.roomList = self._getRoomList(page)

	def _getRoomList(self,page):
		pass
	def start(self):
		#实例化生弹幕成客户端
		liveClients = [BilibiliDanmuClient(roomId, self.loop, self.executor) for roomId in self.roomList]	
		initTasks = []

		for client in liveClients:
			initTasks.append(client.init_socket())
		# 将所有的socket初始连接协程放入队列
		self.loop.run_until_complete(asyncio.gather(*initTasks))
		# 等待连接完成
		print('连接弹幕服务器完成:', len(initTasks))
		# 生成所有的心跳协程和弹幕消息接收协程构成的任务列表
		danmuTasks = []#[testMemory()]
		for client in liveClients:
			#未连接弹幕成功的房间直接略过
			if not client.connected : continue
			danmuTasks.extend([
				asyncio.ensure_future(client.heartCoro()),
				asyncio.ensure_future(client.danmuCoro()),
			])
		try:
			self.loop.run_until_complete(asyncio.gather(*danmuTasks))
			# 持续接收弹幕消息
		except KeyboardInterrupt:
			print('关闭')
		finally:
			# print(">> Cancelling tasks now")
			# for task in asyncio.Task.all_tasks():
			#     task.cancel()
			# self.loop.run_until_complete(asyncio.sleep(1))
			# print(">> Done cancelling tasks")
			self.loop.close()

class BDCManager(DanmuClientManger):
	def _getRoomList(self,page):
		try:
			roomList = room.room
		except Exception as e:
			roomList = GetTopUpRoomId(page[0],page[1]).start()
		return roomList
		
if __name__ == '__main__':
	cm = BDCManager(page=[0,7])
	cm.start()