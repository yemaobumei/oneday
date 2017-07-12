#!/usr/bin/python3  
# -*- coding: utf-8 -*- 
import abc
import socket

class AbstractDanMuClient(metaclass=abc.ABCMeta):
	'''主要流程：
	   先获取直播状态，
	   然后获取弹幕服务器地址与房间信息，
	   之后开启socket连接并认证，
	   最后持续发送心跳包和接收弹幕消息'''

	def __init__(self, roomId, loop, executor):
		self.roomId = roomId
		self.loop = loop
		self.executor = executor
		self.sock = None
		self.connected = False

	@abc.abstractmethod
	def _get_live_status(self):
		'''由直播网页获取主播直播状态'''
		return False

	@abc.abstractmethod
	def _prepare_env(self):
		'''获取弹幕服务器ip和端口号以及房间信息用以认证'''
		return ('0.0.0.0', 80), {}

	def prepare_env(self):
		'''调用self._get_live_status和self._prepare_env完成准备工作'''
		if not self._get_live_status():
			raise Exception(u"直播未开始")
		return self._prepare_env()
	 
	@abc.abstractmethod
	async def _init_socket(self, roomInfo):
		'''具体的socket连接到房间的方式，由子类重写，
		   应使用await self.loop.sock_sendall方式发送数据'''
		self.connected = True

	async def init_socket(self, danmuSocketInfo, roomInfo):
		'''初始化socket并调用self.init_socket方法'''
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.setblocking(False)
		try:
			await self.loop.sock_connect(self.sock, danmuSocketInfo)
		# ConnectionRefusedError
		except Exception as e:
			print(50,e)
		else:
			await self._init_socket(roomInfo)

	@abc.abstractmethod
	async def heartCoro(self):
		'''每隔x秒发送心跳包维持websocket连接'''
		pass

	async def danmuCoro(self):
		'''弹幕处理协程，异步接收弹幕数据
		   并使用self.msgHandleBlock在另一线程/进程处理数据
		   因为数据流是单向的所以即使是进程也不麻烦'''
		while self.connected:
			content = await self.loop.sock_recv(self.sock, 1024)
			# sock_recv(sock[, 1024]) 接收字节不可以省略
			self.loop.run_in_executor(self.executor, self.msgHandleBlock, content)

	@abc.abstractmethod
	def msgHandleBlock(self, content):
		'''阻塞耗时的弹幕数据处理'''
		pass




