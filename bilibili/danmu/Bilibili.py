#!/usr/bin/python3  
# -*- coding: utf-8 -*- 

import re, json, random, time
import requests
import asyncio
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
	def _get_live_status(self):
		url = 'http://live.bilibili.com/%s'%(self.roomId)
		self.roomId = re.findall(b'var ROOMID = (\d+);', requests.get(url).content)[0].decode('utf-8')
		r = requests.get('http://live.bilibili.com/api/player?id=cid:' + self.roomId)
		self.serverUrl = re.findall(b'<server>(.*?)</server>', r.content)[0].decode('utf-8')
		self.dmPort = re.findall(b'<dm_port>(.*?)</dm_port>', r.content)[0].decode('utf-8')        
		return re.findall(b'<state>(.*?)</state>', r.content)[0] == b'LIVE'		
	def _prepare_env(self):
		return (self.serverUrl, self.dmPort), {}

	def prepare_env(self):
			'''调用self._get_live_status和self._prepare_env完成准备工作'''
			if not self._get_live_status():
				raise Exception(u"直播未开始")
			return self._prepare_env()

	async def _init_socket(self, roomInfo):
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
				msg['NickName'] = (msg.get('info', ['','',['', '']])[2][1]
					or msg.get('data', {}).get('uname', ''))
				msg['Content']  = msg.get('info', ['', ''])[1]
				msg['MsgType']  = {'SEND_GIFT': 'gift', 'DANMU_MSG': 'danmu',
					'WELCOME': 'enter'}.get(msg.get('cmd'), 'other')
			except Exception as e:
				pass
			else:

				print(msg['NickName']+msg['Content'],self.roomId) 
				return  
	