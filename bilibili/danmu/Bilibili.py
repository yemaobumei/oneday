#!/usr/bin/python3  
# -*- coding: utf-8 -*- 

import re, json, random, time
import requests
import socket
import asyncio, aiohttp
from struct import pack
from Abstract import AbstractDanMuClient
import sys
sys.path.append('../')
from helper.sql import addFengbao

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
					self.roomId = int(re.findall('var ROOMID = (\d+);', html)[0])
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

	def getJson(self,msg):
		try:
			cmd = re.findall('\"cmd\":(.+?)\,',msg)[0]
			data=re.findall('\"data\":(.+\})\,',msg)[0]
			giftName=re.findall('\"giftName\":(.+?)\,',data)[0]
			uname=re.findall('\"uname\":(.+?)\,',data)[0]
			uid=re.findall('\"uid\":(.+?)\,',data)[0]
			dic={
				"cmd" : cmd,
				"data":{
					"giftName" : giftName,
					"uname" : uname,
					"uid" : uid
				}
			}
		except Exception as e:
			print(113,e)
			dic = {}
		return dic	

	def msgHandleBlock(self, content):
		for msg in re.findall(b'\x00({[^\x00]*})', content):
			try:
				msg = msg.decode('utf8','ignore')
				dic = json.loads(msg)
			except Exception as e:
				print(122,e)
				dic = self.getJson(msg)
				cmd = dic.get('cmd','')
			else:
				cmd = dic['cmd']
			finally:

				if cmd == 'DANMU_MSG':					
					commentText = dic['info'][1]
					commentUser = dic['info'][2][1]
					print (172,commentUser + ' say: ' + commentText,self.roomId)				
					return

				if cmd == 'SEND_GIFT' :

					#获取送礼信息		
					GiftName = dic['data']['giftName']
					send_uid=dic['data']['uid']
					send_uname=dic['data']['uname']
					# if self.roomId == 2570641:
					print(GiftName,self.roomId)
					return

	def sendDanmu(self,roomid,msg,cookies):
		send_url="http://live.bilibili.com/msg/send"
		method="POST"
		data={
			'mode':2,
			'msg':msg,
			'roomid':roomid		
		}
		res = requests.post(send_url,cookies=cookies,data=data)
		if res.status_code==200:
			print('弹幕发送成功')

class BilibiliFengbaoClient(BilibiliDanmuClient):

	def __init__(self, roomId, loop, executor, cookieslist = []):
		super(BilibiliFengbaoClient, self).__init__(roomId, loop, executor)
		self.fengbao = False
		self.send_uid = ""
		self.send_uname= ""
		self.cookieslist = cookieslist


	def msgHandleBlock(self, content):
		for msg in re.findall(b'\x00({[^\x00]*})', content):
			try:
				msg = msg.decode('utf8','ignore')
				dic = json.loads(msg)
			except Exception as e:
				print(179,e)
				dic = self.getJson(msg)
				cmd = dic.get('cmd','')
			else:
				cmd = dic['cmd']
			finally:
				
				if cmd == 'DANMU_MSG':
					if self.fengbao:
						self.fengbao = False					
						commentText = dic['info'][1]
						commentUser = dic['info'][2][1]
						try:
							for cookies in self.cookieslist:
								self.sendDanmu(self.roomId,commentText,cookies)
							print (172,commentUser + ' say: ' + commentText,self.roomId)				
							addFengbao(self.roomId,self.send_uid,self.send_uname)
						except Exception as e:
							print(177,e)
					return

				if cmd == 'SEND_GIFT' :

					#获取送礼信息		
					GiftName = dic['data']['giftName']

					# if self.roomId == 2570641:
					# 	self.fengbao=True
					#print(GiftName,self.roomId)
					if GiftName == "节奏风暴":
						self.send_uid=dic['data']['uid']
						self.send_uname=dic['data']['uname']				
						self.fengbao = True
					return

				