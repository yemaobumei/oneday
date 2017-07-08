#!/usr/bin/python3
#coding=utf-8

import asyncio
import aiohttp
import xml.dom.minidom
import random
import json
from struct import *
import re

#api.py
import os,sys
sys.path.append("../")
import requests
import requests.utils
import pickle
import rsa
import binascii
from bs4 import BeautifulSoup


#helper
import difflib
import math
import datetime,time
import random

from helper.sql import  addFengbao

headers={
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
			'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
		}


class DanmuWebsocket():
	def __init__(self,cookies_list,roomid):
		self._CIDInfoUrl = 'http://live.bilibili.com/api/player?id=cid:'
		self._ChatPort = 788
		self._protocolversion = 1
		self._reader = 0
		self._writer = 0
		self.connected = False
		self._UserCount = 0
		self._ChatHost = 'livecmt-1.bilibili.com'

		self._roomId = roomid
		self._roomId = int(self._roomId)

		self.cookies_list=cookies_list
		self.fengbao=False
		#风暴信息		
		self.i=0
		self.send_uid=0
		self.send_uname=""




			

	async def connectServer(self):
		#print ('正在进入房间。。。。。')
		with aiohttp.ClientSession() as s:
			async with s.get('http://live.bilibili.com/' + str(self._roomId)) as r:
				html = await r.text()
				m = re.findall(r'ROOMID\s=\s(\d+)', html)
				ROOMID = m[0]
			self._roomId = int(ROOMID)
			async with s.get(self._CIDInfoUrl + ROOMID) as r:
				xml_string = '<root>' + await r.text() + '</root>'
				dom = xml.dom.minidom.parseString(xml_string)
				root = dom.documentElement
				server = root.getElementsByTagName('server')
				self._ChatHost = server[0].firstChild.data



		reader, writer = await asyncio.open_connection(self._ChatHost, self._ChatPort)
		self._reader = reader
		self._writer = writer
		# print ('链接弹幕中。。。。。')
		if (await self.SendJoinChannel(self._roomId) == True):
			self.connected = True
			# print ('进入房间成功。。。。。',self._roomId)
			# print ('链接弹幕成功。。。。。')
			await self.ReceiveMessageLoop()
			
	async def HeartbeatLoop(self):
		while self.connected == False:
			await asyncio.sleep(0.5)


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
						#print(258,e)
						continue
					await self.parseDanMu(messages)
					continue
				elif num==5 or num==6 or num==7:
					tmp = await self._reader.read(num2)
					continue
				else:
					if num != 16:
						tmp = await self._reader.read(num2)
					else:
						continue

	async def parseDanMu(self, messages):
		try:

			dic = json.loads(messages)
			cmd = dic['cmd']

		except Exception as e: # 有些情况会 jsondecode 失败，未细究，可能平台导致
			# print(276,e)
			# print(type(messages),messages)
			return
		
		if cmd == 'DANMU_MSG':

			if self.fengbao:					
				commentText = dic['info'][1]
				commentUser = dic['info'][2][1]
				try:
					print (311,commentUser + ' say: ' + commentText,self._roomId)
					await self.sendDanmu(commentText)
					self.fengbao=False
					await self.addFengbaoProxy(self._roomId,self.send_uid,self.send_uname)
					return						
				except Exception as e:
					self.fengbao=False
					print(314,e)
				return
		if cmd == 'SEND_GIFT' :


			#获取送礼信息		
			GiftName = dic['data']['giftName']
			# uid=dic['data']['uid']
			# gifts=['B坷垃','喵娘','节奏风暴','普通拳']
			# gifts_low=['233','666','小拳拳','亿圆']
			#print (332,GiftName,GiftNum)
			self.send_uid=dic['data']['uid']
			self.send_uname=dic['data']['uname']

			try:
				if GiftName == "节奏风暴":				
					self.fengbao = True
					print(GiftName,self._roomId)
			except Exception as e:
				print(355,e,GiftUser)
			return

#---辅助弹幕部分--------------------------------------------------------------------------

	async def sendDanmu(self,msg):
		send_url="http://live.bilibili.com/msg/send"
		method="POST"
		msg=msg.strip()
		if len(msg) == 0:
			return
		data={
			'color':'16772431',
			'fontsize':25,
			'mode':1,
			'msg':msg,
			'rnd':'1493972251',
			'roomid':self._roomId     
		}
		for cookies in self.cookies_list:
			# async with  aiohttp.ClientSession(cookies=cookies) as s:
			# 	async with  s.post(send_url,headers=headers,data=data) as res:
			# 		await res.text()
			# 		print("send danmu ok!")

					# if res.status==200:
					# 	print(108,msg,self._roomId)
			#os.system("nohup python3 -c \"import requests;requests.post(\'%s\',cookies=%s,headers=%s,data=%s)\" >danmu.out 2>&1 &"%(send_url,cookies,headers,data))
			requests.post(send_url,cookies=cookies,headers=headers,data=data)
		await asyncio.sleep(0.01)

	async def addFengbaoProxy(self,realRoomid,send_uid,send_uname):
		await asyncio.sleep(2)
		addFengbao(realRoomid,send_uid,send_uname)
		print("fengbao success!")