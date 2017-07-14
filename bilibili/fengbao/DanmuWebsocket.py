#!/usr/bin/python3
#coding=utf-8

import asyncio, aiohttp
import xml.dom.minidom
import random
import json
import re

#api.py
import os,sys
sys.path.append("../")
import requests
from struct import *


#helper
import time
from helper.sql import  addFengbao

headers={
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
			'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
		}


class DanmuWebsocket():
	def __init__(self,loop,cookies_list,roomid):
		self._CIDInfoUrl = 'http://live.bilibili.com/api/player?id=cid:'
		self._ChatPort = 2243#788
		self._protocolversion = 1
		self._reader = 0
		self._writer = 0
		self.connected = False
		self._UserCount = 0
		self._ChatHost = 'livecmt-2.bilibili.com'

		self.loop = loop
		self._roomId = int(roomid)
		self.cookies_list=cookies_list

		#风暴信息	
		self.fengbao=False			
		self.send_uid=0
		self.send_uname=""			

	async def connectServer(self):
		try:
			# #print ('正在进入房间。。。。。')
			# with aiohttp.ClientSession() as s:
			# 	async with s.get('http://live.bilibili.com/' + str(self._roomId)) as r:
			# 		html = await r.text()
			# 		m = re.findall(r'ROOMID\s=\s(\d+)', html)
			# 		ROOMID = m[0]#str
			# 	self._roomId = int(ROOMID)
			# 	async with s.get(self._CIDInfoUrl + ROOMID) as r:
			# 		xml_string = '<root>' + await r.text() + '</root>'
			# 		dom = xml.dom.minidom.parseString(xml_string)
			# 		root = dom.documentElement
			# 		server = root.getElementsByTagName('server')
			# 		self._ChatHost = server[0].firstChild.data
			pass
		except Exception as e:
			self.connected	=	False
			print(84,e,self._roomId)

		else:
			reader, writer = await asyncio.open_connection(self._ChatHost, self._ChatPort)
			self._reader = reader
			self._writer = writer
			# print ('链接弹幕中。。。。。')
			if (await self.SendJoinChannel(self._roomId) == True):
				self.connected = True
				print ("链接房间:%s成功"%(self._roomId))
				await self.ReceiveMessageLoop()			
			else:
				print("链接房间:%s失败"%(self._roomId))
				



	async def HeartbeatLoop(self):
		# while self.connected == False:
		# 	await asyncio.sleep(0.5)

		while self.connected == True:
			await self.SendSocketData(0, 16, self._protocolversion, 2, 1, "")
			await asyncio.sleep(30)


	async def SendJoinChannel(self, channelId):
		self._uid = (int)(100000000000000.0 + 200000000000000.0*random.random())
		body = '{"roomid":%s,"uid":%s}' % (channelId, self._uid)
		await self.SendSocketData(0, 16, self._protocolversion, 7, 1, body)
		return True


	async def SendSocketData(self, packetlength, magic, ver, action, param, body):
		bytearr = body.encode('utf-8')
		if packetlength == 0:
			packetlength = len(bytearr) + 16
		sendbytes = pack('!IHHII', packetlength, magic, ver, action, param)
		if len(bytearr) != 0:
			sendbytes = sendbytes + bytearr
		self._writer.write(sendbytes)
		await self._writer.drain()


	async def ReceiveMessageLoop(self):
		while self.connected == True:
			try:
				tmp = await self._reader.read(4)
				expr, = unpack('!I', tmp)
				tmp = await self._reader.read(2)
				tmp = await self._reader.read(2)
				tmp = await self._reader.read(4)
				num, = unpack('!I', tmp)
				tmp = await self._reader.read(4)
				num2 = expr - 16

				if num2 != 0:
					num -= 1
					if num==0 or num==1 or num==2:
						tmp = await self._reader.read(4)
						num3, = unpack('!I', tmp)
						#print ('房间人数为 %s' % num3)
						self._UserCount = num3
						continue
					elif num==3 or num==4:
						tmp = await self._reader.read(num2)
						# strbytes, = unpack('!s', tmp)
						try: # 为什么还会出现 utf-8 decode error??????
							messages = tmp.decode('utf-8')
						except Exception as e:
							#print(147,e)
							continue
						await self.parseDanMu(messages)
					elif num==5 or num==6 or num==7:
						tmp = await self._reader.read(num2)
						continue
					else:
						if num != 16:
							tmp = await self._reader.read(num2)
						else:
							continue
			except Exception as e:
				pass
				#print(161,"DanmuWebsocket.py:161",e)			

	def getJson(self,msg):
		def find(result):
			if len(result)!=0:
				return result[0]
			else:
				return "0000"
		try:
			cmd = find(re.findall('"cmd":["]?(.+?)["]?\,',msg))
			#print(cmd=='SEND_GIFT')
			if cmd != 'SEND_GIFT': return {}
			giftName = find(re.findall('"giftName":["]?(.+?)["]?\,',msg))
			uname = find(re.findall('"uname":["]?(.+?)["]?\,',msg))
			uid = int(find(re.findall('"uid":["]?(.+?)["]?\,',msg)))
			dic = {
				"cmd" : cmd,
				"data":{
					"giftName" : giftName,
					"uname" : uname,
					"uid" : uid
				}
			}
		except Exception as e:
			print(113,msg)
			dic = {}
		return dic

	async def parseDanMu(self, messages):
		try:

			dic = json.loads(messages)
			#print(dic)
			#cmd = dic['cmd']

		except Exception as e: # 有些情况会 jsondecode 失败，未细究，可能平台导致
			#print(276,e)
			dic = self.getJson(messages)
			#print(dic)
 
		cmd = dic.get('cmd','')
		
		if cmd == 'DANMU_MSG':
			if self.fengbao:					
				commentText = dic['info'][1]
				commentUser = dic['info'][2][1]
				try:
					await self.sendDanmu(commentText)
					self.fengbao = False
					print (172,commentUser + ' say: ' + commentText,self._roomId)				
					#self.loop.run_in_executor(None,addFengbao,*[self._roomId,self.send_uid,self.send_uname])
					#数据库操作不能同时放入多个线程。
					addFengbao(self._roomId,self.send_uid,self.send_uname)
				except Exception as e:
					print(177,e)
			return

		if cmd == 'SEND_GIFT' :
			data = dic.get('data','')
			#获取送礼信息		
			GiftName = data.get('giftName',"noGiftName")
			# if self._roomId == 2570641:
			# 	print(GiftName,self._roomId)
			# 	self.fengbao=True
			if GiftName == "节奏风暴":
				self.send_uid = data.get('uid',0)
				self.send_uname = data.get('uname','noSendname')			
				self.fengbao = True
			return

#---辅助弹幕部分--------------------------------------------------------------------------

	async def sendDanmu(self,msg):
		send_url="http://live.bilibili.com/msg/send"
		method="POST"
		msg=msg.strip()
		if len(msg) == 0:
			return
		data={
			# 'color':'16772431',
			# 'fontsize':25,
			# 'mode':1,
			'msg':msg,
			# 'rnd':int(time.time()),#'1493972251',
			'roomid':self._roomId     
		}
		for cookies in self.cookies_list:
			async with  aiohttp.ClientSession(cookies=cookies) as s:
				async with  s.post(send_url,headers=headers,data=data) as res:
					await res.text()
					#r=json.loads(res.text())
					#print('send danmu ok!',r['msg'])
					# if res.status==200:
					# 	print(108,msg,self._roomId)
					
			#os.system("nohup python3 -c \"import requests;requests.post(\'%s\',cookies=%s,headers=%s,data=%s)\" >danmu.out 2>&1 &"%(send_url,cookies,headers,data))
			#requests.post(send_url,cookies=cookies,headers=headers,data=data)
		#await asyncio.sleep(0.01)
