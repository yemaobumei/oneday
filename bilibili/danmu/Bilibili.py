#!/usr/bin/python3  
# -*- coding: utf-8 -*- 

import re, json, random, time
import requests
import socket
import asyncio, aiohttp
from struct import pack
from Abstract import AbstractDanMuClient

# import socket
# class _socket(socket.socket):
# 	def push(self, data, type = 7):
# 		data = (pack('>i', len(data) + 16) + b'\x00\x10\x00\x01' +
# 			pack('>i', type) + pack('>i', 1) + data)
# 		self.sendall(data)
# 	def pull(self):
# 		try: # for socket.settimeout
# 			return self.recv(9999)
# 		except Exception as e:
# 			return ''
class BilibiliDanmuClient(AbstractDanMuClient):
	def __init__(self, roomId, loop, executor):
		super(BilibiliDanmuClient, self).__init__(roomId,loop,executor)
		self.serverUrl = "livecmt-2.bilibili.com"
		self.dmPort = 2243

	async def _get_live_status(self):
		try:
			liveUrl = 'http://live.bilibili.com/%s'%(self.roomId)
			CIDURL = 'http://live.bilibili.com/api/player?id=cid:%s'%(self.roomId) 
			with aiohttp.ClientSession() as s:
				async with s.get(liveUrl) as r:
					html = await r.text()#r.text()返回结果是经过编码的,r.read未编码 b''
					#获取真实房间号		
					self.roomId = re.findall('var ROOMID = (\d+);', html)[0]
			async with aiohttp.ClientSession() as s:
				async with s.get(CIDURL) as r:
					lxml = await r.text()
					self.serverUrl = re.findall('<server>(.*?)</server>', lxml)[0]
					self.dmPort = re.findall('<dm_port>(.*?)</dm_port>', lxml)[0]        
					return re.findall('<state>(.*?)</state>', lxml)[0] == 'LIVE'
		except Exception as e:
			print("Bilibili.py:43",e)
			return False		


	async def _prepare_env(self):
		'''调用self._get_live_status和self._prepare_env完成准备工作'''
		# status = await self._get_live_status()
		# if  not status : return False
		#暂时不用，否则同时同时发生get请求太多无效。
		return (self.serverUrl, self.dmPort)

	async def _init_socket(self):
		try:
			data = json.dumps({
				'roomid': int(self.roomId),
				'uid': int(1e14 + 2e14 * random.random()),
				}, separators=(',', ':')).encode('ascii')
			type = 7
			data = (pack('>i', len(data) + 16) + b'\x00\x10\x00\x01' +
				pack('>i', type) + pack('>i', 1) + data)
			await self.loop.sock_sendall(self.sock, data)
		except Exception as e:
			print(52,e)
			self.connected = False
			self.sock.close()
		else:
			self.connected = True
			print("连接成功:%s"%(self.roomId))

	async def init_socket(self):
		'''初始化socket并调用self.init_socket方法'''
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.setblocking(False)
		danmuSocketInfo = await self._prepare_env()
		if danmuSocketInfo == False : return
		try:
			await self.loop.sock_connect(self.sock, danmuSocketInfo)
		# ConnectionRefusedError
		except Exception as e:
			print("Bilibili.py:81",e)
			return False
		else:
			await self._init_socket()

	#保持socket心跳
	async def heartCoro(self):
		type = 2
		data=b""
		data = (pack('>i', len(data) + 16) + b'\x00\x10\x00\x01' +
			pack('>i', type) + pack('>i', 1) + data)
		while True:
			await self.loop.sock_sendall(self.sock,data)
			await asyncio.sleep(30)

	def msgHandleBlock(self, content):
		for msg in re.findall(b'\x00({[^\x00]*})', content):
			try:
				msg = json.loads(msg.decode('utf8', 'ignore'))
				cmd = msg['cmd']
				msg['NickName'] = (msg.get('info', ['','',['', '']])[2][1]
					or msg.get('data', {}).get('uname', ''))
				msg['Content']  = msg.get('info', ['', ''])[1]
				msg['MsgType']  = {'SEND_GIFT': 'gift', 'DANMU_MSG': 'danmu',
					'WELCOME': 'enter'}.get(msg.get('cmd'), 'other')
			except Exception as e:
				pass
			else:
				#print(msg['NickName']+'say: '+msg['Content'],self.roomId) 
				return  
	