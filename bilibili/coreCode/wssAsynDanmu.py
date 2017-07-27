#!/usr/bin/python3
#encoding=utf-8
from websockets import connect
import time
import random
import json
import re
import requests
from struct import *
import asyncio, aiohttp


class WebSocketDanmu():

	def __init__(self, roomid = 2570641, useDanmuType = "ws"):

		self.roomid = int(roomid)
		self.useDanmuType = useDanmuType

		##websocket
		#`${WSSDMPROTOCOL}://${WSDMSERVER}:${WSSDMPORT}/${WSDMPATH}`
		self.wsurl = "ws://broadcastlv.chat.bilibili.com:2244/sub"	
		self.wssurl = "wss://broadcastlv.chat.bilibili.com:2245/sub"
		

		##tcp连接读写接口
		self._reader = ""
		self._writer = ""

		##
		self.ws = None
		self.connected = False

	##获取主播真实房间号
	async def getRealRommId(self):
		async with aiohttp.ClientSession() as s:
			async with s.get('http://live.bilibili.com/' + str(self.roomid)) as r:
				html = await r.text()
				m = re.findall(r'ROOMID\s=\s(\d+)', html)
				self.roomid = int(m[0])#str

	#"服务器推送数据"
	async def push(self, data = b'', type = 7):
		try:
			data = (pack('>i', len(data) + 16) + b'\x00\x10\x00\x01' + pack('>i', type) + pack('>i', 1) + data)
			if self.useDanmuType == "ws" or self.useDanmuType == "wss":
				await self.ws.send(data)
			else: #tcp
				self._writer.write(data)
				await self._writer.drain()
		except Exception as e:
			print(32,e)	

	#弹幕池心跳包	
	async def heartBeat(self):
		while self.connected == False:
			await asyncio.sleep(1)

		while self.connected == True:
			await self.push(data = b'', type = 2)
			await asyncio.sleep(30)

	#发送弹幕池连接验证信息
	async def sendJoinRoom(self):
		data = json.dumps({
			'roomid': self.roomid,
			'uid': int(1e14 + 2e14 * random.random()),
			}, separators=(',', ':')).encode('ascii')
		await self.push(data = data, type = 7)
		self.connected = True

	async def tcpReceiveDanmu(self):
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
				return 
			elif num==3 or num==4:
				tmp = await self._reader.read(num2)
				# strbytes, = unpack('!s', tmp)
				try: # 为什么还会出现 utf-8 decode error??????
					messages = tmp.decode('utf-8')
				except:
					return 
				else:
					# await self.parseDanMu(messages)
					return messages
				print(tmp)
				return tmp
			elif num==5 or num==6 or num==7:
				tmp = await self._reader.read(num2)
				return 
			else:
				if num != 16:
					tmp = await self._reader.read(num2)
				else:
					return 
		return 
	async def receiveMessageLoop(self):
		while self.connected == True:
			try:
				if self.useDanmuType == 'tcp':
					bmessage = await self.tcpReceiveDanmu()
				else:
					bmessage = await self.ws.recv()
				if not bmessage:
					continue
			except Exception as e:
				self.connected = False
				if self.useDanmuType == "tcp":
					self._writer.close()
				else:
					self.ws.close()
				break
			else:
				await self.parseDanmu(bmessage)
		await self.start()	
	async def parseDanmu(self, message):
		dic = {}	
		try:
			if self.useDanmuType == "tcp":
				dic = json.loads(message)
			else:
				for msg in re.findall(b'\x00({[^\x00]*})', message):
					msg = msg.decode('utf-8','ignore')
					dic = json.loads(msg)
					await self.handlerMessage(dic)
		except Exception as e:
			print(141,e)

	async def handlerMessage(self,dic):
		cmd = dic.get('cmd','')

		if cmd == 'DANMU_MSG':					
			commentText = dic['info'][1]
			commentUser = dic['info'][2][1]
			print (commentUser + ' say: ' + commentText)				
			return

		if cmd == 'SEND_GIFT' :
			data = dic.get('data','')
			#获取送礼信息		
			GiftName = data['giftName']
			GiftUser = data['uname']
			Giftrcost = data['rcost']
			GiftNum = data['num']
			uid = data['uid']
			msg = "%s 赠送 %sx%s"%(GiftUser,GiftName,GiftNum)
			print(msg)
			return
	async def start(self):
		##获取主播真实房间号
		await self.getRealRommId()
		##选择连接弹幕池的方式
		if self.useDanmuType == 'ws':
			self.ws = await connect(self.wsurl)
		elif self.useDanmuType == "wss":
			self.ws = await connect(self.wssurl)
		else:
			self._reader, self._writer = await asyncio.open_connection('livecmt-2.bilibili.com', 2243)
	
		await self.sendJoinRoom()
		await self.receiveMessageLoop()








if __name__ == "__main__":
	
	
	room = [193520]#771423,
	tasks = []
	for each in room:
		danmuji = WebSocketDanmu(roomid = each, useDanmuType = 'wss')
		tasks += [ danmuji.start(), danmuji.heartBeat(), ]
	
	try:
		loop = asyncio.get_event_loop()
		loop.run_until_complete(asyncio.wait(tasks))
	except KeyboardInterrupt:
		print("手动关闭")
	finally:
		# print(">> Cancelling tasks now")
		for task in asyncio.Task.all_tasks():
			task.cancel()
		loop.run_until_complete(asyncio.sleep(1))
		print(">> Done cancelling tasks")
		loop.close()

