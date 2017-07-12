#!/usr/bin/python3  
# -*- coding: utf-8 -*-  

import asyncio
import concurrent.futures
from getTopUp import GetTopUpRoomId
from Bilibili import BilibiliDanmuClient

async def testMemory():
	# 测试内存占用
	import os
	import psutil
	while True:
		process = psutil.Process(os.getpid())
		print(os.getpid(), '占用',
			str(process.memory_info().rss / 1024 / 1024))
		await asyncio.sleep(10)


class DanmuClientManger():
	"""docstring for ClassName"""
	def __init__(self, loop = None, executor = None, page = [0,7]):
		#私有一个事件循环控制器
		self.loop = loop or asyncio.get_event_loop()
		#私有一个cpu占用型任务的线程池
		self.executor = executor or concurrent.futures.ThreadPoolExecutor(max_workers=2,) 
		
		# 得到需要连接的直播房间列表
		self.roomList = self._getRoomList(page)

	def _getRoomList(self,page):
		pass
	def start(self):
		#实例化生弹幕成客户端
		clientList=[BilibiliDanmuClient(roomId, self.loop, self.executor) for roomId in self.roomList]	
		initTasks = []
		liveClients = []
		for client in clientList:
			try:
				danmuSocketInfo, roomInfo = client.prepare_env()
				# 完成准备工作，生成弹幕服务器信息和房间信息
			except Exception as e:
				print(e)
				print("某主播不在线-", client.roomId)
			else:
				liveClients.append(client)
				initTasks.append(client.init_socket(danmuSocketInfo, roomInfo))
		# 将所有的socket初始连接协程放入队列
		self.loop.run_until_complete(asyncio.gather(*initTasks))
		# 等待连接完成
		print('连接弹幕服务器完成:', len(initTasks))
		# 生成所有的心跳协程和弹幕消息接收协程构成的任务列表
		danmuTasks = [testMemory()]
		for client in liveClients:
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
		return GetTopUpRoomId(page[0],page[1]).start()
		
if __name__ == '__main__':
	cm = BDCManager(page=[0,1])
	cm.start()