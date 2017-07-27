#!/usr/bin/python3
#encoding=utf-8
import sys
sys.path.append("../")
from helper.sql import addFengbao
from websockets import connect
import time
import random
import json
import re
import requests
from struct import *
import asyncio, aiohttp

headers={
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
			'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
		}

class BaseWebSocketDanmuClient():

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
				self.roomid = int(m[0]) #str

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
		print("连接直播间:%s弹幕成功"%(self.roomid))

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
			print (self.roomid, commentUser + ' say: ' + commentText)				
			return

		if cmd == 'SEND_GIFT' :
			data = dic.get('data','')
			##获取送礼信息		
			giftName = data['giftName']
			giftUser = data['uname']
			giftrcost = data['rcost']
			giftNum = data['num']
			uid = data['uid']
			msg = "%s 赠送 %sx%s"%(giftUser,giftName,giftNum)
			print(self.roomid, msg)
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

##---------批量房间弹幕基础管理器----------------------------------------
class BaseClientManager():

	def __init__(self, roomList = [ 2570641, ], useDanmuType = 'ws'):
		self.roomList = roomList
		self.useDanmuType = useDanmuType

	def _prepare(self):
		pass

	def getTasks(self):
		tasks = []	
		for each in self.roomList:
			task = BaseWebSocketDanmuClient(roomid = each, useDanmuType = self.useDanmuType)
			tasks += [ task.start(), task.heartBeat() ]
		return tasks

	def start(self):
		tasks = self.getTasks()	
		try:
			loop = asyncio.get_event_loop()
			loop.run_until_complete(asyncio.wait(tasks))
		except KeyboardInterrupt:
			print("手动关闭")
		finally:
			print(">> Cancelling tasks now")
			for task in asyncio.Task.all_tasks():
				task.cancel()
			loop.run_until_complete(asyncio.sleep(1))
			print(">> Done cancelling tasks")
			loop.close()		



##------单个房间风暴客户端-----------------------------------------
class BeatStormClient(BaseWebSocketDanmuClient):

	def __init__(self, cookies_list = [], record = False, roomid = 2570641, useDanmuType = "ws"):
		super(BeatStormClient, self).__init__(roomid=roomid, useDanmuType = useDanmuType)
		self.cookies_list = cookies_list 
		self.record = record

	async def handlerMessage(self,dic):
		cmd = dic.get('cmd','')
		if cmd == 'SEND_GIFT' :
			data = dic.get('data','')
			#获取送礼信息		
			giftName = data['giftName']
			# print(self.roomid,giftName)
			if giftName == "节奏风暴":
				try:
					send_uid = data.get('uid',0)
					send_uname = data.get('uname','noSendname')			
					fengbaoId = data['specialGift']['39']['id']
					content = data['specialGift']['39']['content']
					await self.sendDanmu(content)
					print(send_uname+'say:'+content)
					if self.record:
						addFengbao(fengbaoId,self.roomid,send_uid,send_uname,content)
				except Exception as e:
					print(213,e)
			return
		
#---辅助弹幕部分--------------------------------------------------------------------------

	async def sendDanmu(self,msg):
		send_url="http://live.bilibili.com/msg/send"
		method="POST"
		if len(msg) == 0:
			return
		data={
			# 'color':'16772431',
			# 'fontsize':25,
			# 'mode':1,
			'msg':msg,
			# 'rnd':int(time.time()),#'1493972251',
			'roomid':self.roomid     
		}
		try:
			for cookies in self.cookies_list:
				async with  aiohttp.ClientSession(cookies=cookies) as s:
					async with  s.post(send_url,headers=headers,data=data) as res:
						await res.text()
						r = await res.text()
						print(r)
						r=json.loads(r)
						

		except Exception as e:
			print("发送弹幕失败!")

##------批量房间风暴客户端管理器-----------------------------------------
class BeatStormClientManager(BaseClientManager):
	"""docstring for BeatStormClientManager"""
	def __init__(self, cookies_list = [], record = False, roomList = [2570641], useDanmuType = "ws"):
		super(BeatStormClientManager, self).__init__(roomList = roomList, useDanmuType = useDanmuType)
		self.cookies_list = cookies_list
		self.record = record

	def getTasks(self):
		tasks = []	
		for each in self.roomList:
			task = BeatStormClient(cookies_list = self.cookies_list, record = self.record, roomid = each, useDanmuType = self.useDanmuType)
			tasks += [ task.start(), task.heartBeat() ]
		return tasks

		


if __name__ == "__main__":
	
###-------批量房间弹幕监控-----------------------------------------	
	# roomList = [ 1273106, 80397 ]#771423,
	# danmuClientManager = BaseClientManager(roomList = roomList)	
	# danmuClientManager.start()

##--------批量房间风暴监控-----------------------------------------
	import room
	from helper.api import Client,MyError
	from getTopUp import GetTopUpRoomId
	
	#登录B站获取cookies	
	info = [
	#	{'username':'13126772351','password':'ye06021123','roomid':4416185},
		{'username':'979365217@qq.com','password':'ye06021123','roomid':2570641},
	#	{'username':'13375190907','password':'licca0907','roomid':2570641},
	#	{'username':'13390776820','password':'wsglr3636...','roomid':2570641},
	#	{'username':'15675178724','password':'zero082570X','roomid':4416185},
	#	{'username':'15130169870','password':'30169870.','roomid':4416185}
	]

	cookies_list = []
	for each in info:		
		LoginClient=Client(each['username'],each['password'])
		cookies,nickname=LoginClient.cookies_login() #<class set (1,2)>
		if not LoginClient.isLogin:
			raise MyError('登陆失败')
		cookies_list.append(cookies)


	#获取最新热门直播房间号
	try:
		roomList = room.room
		if len(roomList) == 0:
			raise MyError("最新热门房间号为空!")
	except Exception as e:
		roomList = GetTopUpRoomId(0,7).start()
	print(len(roomList))

	#开启节奏风暴管理器
	BSCM = BeatStormClientManager(cookies_list = cookies_list, record = True, roomList = roomList, useDanmuType = "ws")
	BSCM.start()

