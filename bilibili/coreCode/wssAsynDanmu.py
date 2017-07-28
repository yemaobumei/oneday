#!/usr/bin/python3
#encoding=utf-8
import sys,os
sys.path.append("../")
from helper.sql import addFengbao
from helper.api import Client,MyError
from websockets import connect

import json
import re
import requests
from struct import *
import asyncio,aiohttp

#helper
import difflib
import math
import datetime,time
import random

headers={
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/51.0.2704.103 Safari/537.36',
			'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
		}

###------------------------基础单房间弹幕获取客户端----------------------------------------------------------
class BaseWebSocketDanmuClient():

	def __init__(self,roomid = 2570641,useDanmuType = "ws"):

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
				m = re.findall(r'ROOMID\s=\s(\d+)',html)
				self.roomid = int(m[0]) #str

	#"服务器推送数据"
	async def push(self,data = b'',type = 7):
		try:
			data = (pack('>i',len(data) + 16) + b'\x00\x10\x00\x01' + pack('>i',type) + pack('>i',1) + data)
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
			await self.push(data = b'',type = 2)
			await asyncio.sleep(30)

	#发送弹幕池连接验证信息
	async def sendJoinRoom(self):
		data = json.dumps({
			'roomid': self.roomid,
			'uid': int(1e14 + 2e14 * random.random()),
			},separators=(',',':')).encode('ascii')
		await self.push(data = data,type = 7)
		self.connected = True
		print("连接直播间:%s弹幕成功"%(self.roomid))

	async def tcpReceiveDanmu(self):
		tmp = await self._reader.read(4)
		expr,= unpack('!I',tmp)
		tmp = await self._reader.read(2)
		tmp = await self._reader.read(2)
		tmp = await self._reader.read(4)
		num,= unpack('!I',tmp)
		tmp = await self._reader.read(4)
		num2 = expr - 16

		if num2 != 0:
			num -= 1
			if num==0 or num==1 or num==2:
				tmp = await self._reader.read(4)
				num3,= unpack('!I',tmp)
				#print ('房间人数为 %s' % num3)
				self._UserCount = num3
				return 
			elif num==3 or num==4:
				tmp = await self._reader.read(num2)
				# strbytes,= unpack('!s',tmp)
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
	async def parseDanmu(self,message):
		dic = {}	
		try:
			if self.useDanmuType == "tcp":
				dic = json.loads(message)
			else:
				for msg in re.findall(b'\x00({[^\x00]*})',message):
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
			print (self.roomid,commentUser + ' say: ' + commentText)				
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
			print(self.roomid,msg)
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
			self._reader,self._writer = await asyncio.open_connection('livecmt-2.bilibili.com',2243)
	
		await self.sendJoinRoom()
		await self.receiveMessageLoop()


##---------批量房间弹幕基础管理器----------------------------------------
class BaseClientManager():

	def __init__(self,roomList = [ 2570641,],useDanmuType = 'ws'):
		self.roomList = roomList
		self.useDanmuType = useDanmuType

	def _prepare(self):
		pass

	def getTasks(self):
		tasks = []	
		for each in self.roomList:
			task = BaseWebSocketDanmuClient(roomid = each,useDanmuType = self.useDanmuType)
			tasks += [ task.start(),task.heartBeat() ]
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

##---------单个房间自动回复弹幕姬----------------------------------------------
class DanmuJi(BaseWebSocketDanmuClient):
	"""docstring for DanmuJi"""
	def __init__(self,username,roomid = 2570641,useDanmuType = "ws"):
		super(DanmuJi,self).__init__(roomid = roomid,useDanmuType = useDanmuType)
		self.cookies,self.nickname = Client(username).cookies_login() 


#---辅助弹幕部分--------------------------------------------------------------------------
		self.gift_dic={}
		self.gift_num=0
		self.recevie_danmu_num = 0

		self.database={
		 	'电影名':'视频右上角电影名',
			'录播':'挂机直播，主播一般不在',
			'gay玩弹幕姬':'放马过来调戏我',
			'今晚日常修仙吗':'不要修仙哟，对身体不好呢',
			'夜猫大佬不在了去哪了':'不要趁我不在就gay我',
			'怎么戴勋章':'pc端右下角发送弹幕框下有个"勋"字,手机端直播中心我的勋章',	
		}
		self.setTimeDanmu=[ '大家可以@夜猫和我聊天哟,我可是百事通呢',
							'喜欢主播右上角点点关注,送点小礼物帮主播升升级',
							'喜欢主播的大佬可以上波船,船上风景别有一番滋味呢',
							'点关注不迷路，主播带你上高速',
						]

	async def sendDanmu(self,msg):
		# print(252,msg)
		send_url="http://live.bilibili.com/msg/send"
		method="POST"
		if len(msg) == 0:
			return
		if len(msg) > 30:
			await self.send_long_danmu(msg)
			return
		data={
			'color':'16772431',
			'fontsize':25,
			'mode':1,
			'msg':msg,
			'rnd':'1493972251',
			'roomid':self.roomid   
		}
		async with  aiohttp.ClientSession(cookies=self.cookies) as s:
			async with  s.post(send_url,headers=headers,data=data) as res:
				result = await res.text() #json字符串


	#### 得到一定等级才能发30个字数的弹幕,注意-----------
	async def send_long_danmu(self,msg):
		length=len(msg)
		c=math.ceil(length/30.0)
		for i in range(c):		
			await self.sendDanmu(msg[i*30:(i+1)*30])
			await asyncio.sleep(1)
					
	async def robot(self,username,msg):
		s=['夜猫','弹幕姬','弹幕机','机器猫']#'主播','喵咭',
		danmu_liyi=['胸','奶子','脱衣','鸡巴']
		data={'info':msg,'key':'a85845213d8f41fc9685fff9c675ec5d'}
		#data={'info':msg,'key':'fef3ad124da348419db60d502d43bcf2'}
		url="http://www.tuling123.com/openapi/api"
		temp_ratio = 0
		temp_key=""
		try:
			if any([1 for i in danmu_liyi if i in msg]):
				await self.sendDanmu('请大家注意弹幕礼仪')
				return
			if '晚安' in msg :				
				if '晚安'!= msg and '主播晚安'!= msg and '喵咭晚安' != msg:
					return
				await self.sendDanmu(username+'晚安') 
				return
			if '去睡' in msg :
				await self.sendDanmu(username+'晚安')
				return
			for key in self.database:
				seq = difflib.SequenceMatcher(None, msg,key)
				ratio = seq.ratio()
				if ratio > temp_ratio :
					temp_ratio = ratio
					temp_key = key
		except Exception as e:
			print(145,e)
	
		if (temp_ratio > 0.49 and len(msg) <= 10) or (temp_ratio > 0.34 and len(msg) > 10) or (temp_ratio >0.2 and len(msg)>20) :
			await self.sendDanmu(self.database[temp_key])
			return
		else:
			contains=[each for each in s if each in msg]
			if any(contains):
				#去掉夜猫，弹幕姬，关键字
				for con in contains:
					msg=msg.replace(con,' ')
				data['info'] = msg
				# s = requests.session()
				# r=requests.post(url,data=data,timeout=2)
				# response=json.loads(r.content.decode('utf-8'))['text']
				try:
					async with  aiohttp.ClientSession() as s:
						async with  s.post(url,headers=headers,data=data,timeout=2) as res:
							r = await res.text()
							response = json.loads(r).get('text','TuLing no Response!')			
					await self.sendDanmu(response+'@'+username)
				except Exception as e:
					print(329,e)

		return

	async def handlerMessage(self,dic):
		cmd = dic.get('cmd','')
		# if cmd == 'LIVE':
		# 	try:
		# 		await self.sendDanmu('小可爱晚上好,小夜猫终于等到你开播了') 
		# 		await self.sendDanmu('欢迎来到直播间'+str(dic['roomid'])+',弹幕姬小夜猫陪伴你们左右')
		# 	except Exception as e:
		# 		print(286,e)
		# 	return
		# if cmd == 'PREPARING':
		# 	try:
		# 		#print ('房主准备中。。。') #{'cmd': 'PREPARING', 'roomid': 2570641}
		# 		await self.sendDanmu('各位晚安,让我们明天继续相约直播间'+str(dic['roomid'])+',明天见')
		# 	except Exception as e:
		# 		print(292,e) 
		# 	return
		if cmd == 'DANMU_MSG':
			self.recevie_danmu_num+=1
			if self.recevie_danmu_num % 40 == 0:
				le=len(self.setTimeDanmu)
				rand=random.randint(0,le-1)
				try:
					await self.sendDanmu(self.setTimeDanmu[rand])
				except Exception as e:
					pass
			commentText = dic['info'][1]
			commentUser = dic['info'][2][1]
			isAdmin = dic['info'][2][2] == '1'
			isVIP = dic['info'][2][3] == '1'
			###----弹幕回复拓展功能-----------
			# print(commentText)
			await self.extended_func(commentText)
			if self.nickname == commentUser:
				return 
			if isAdmin:
				commentUser = '管理员 ' + commentUser
			if isVIP:
				commentUser = 'VIP ' + commentUser
			try:
				# print (311,commentUser + ' say: ' + commentText)
				await self.robot(commentUser,commentText)
			except Exception as e:
				print(314,e)
			return
		if cmd == 'SEND_GIFT':
			#累计多次礼物后，情况礼物清单栏,{'a':3,'b':5}
			self.gift_num+=1
			if self.gift_num % 50 == 0:
				self.gift_dic={}
				await self.sendDanmu('谢谢大家的关注和礼物,弹幕滑动太快主播可能会漏看,多见谅')
			#获取送礼信息		
			GiftName = dic['data']['giftName'].strip()
			GiftUser = dic['data']['uname']
			Giftrcost = dic['data']['rcost']
			GiftNum = dic['data']['num']
			uid=dic['data']['uid']
			gifts=['B坷垃','喵娘','节奏风暴','普通拳']
			gifts_low=['233','666','小拳拳','亿圆']
			res=""
			#print (332,GiftName,GiftNum)

			#单次送礼记录礼物清单内，连续多次后触发不弹幕'打包投喂'。
			try:
				if GiftNum==1:
					if not uid in self.gift_dic:
						self.gift_dic[uid]={'uname':GiftUser,'num':1}
					else:	
						self.gift_dic[uid]['num']	+= 1					
					if self.gift_dic[uid]['num'] >= 6:
						self.gift_dic[uid]['num'] = 0
						res='谢谢'+GiftUser+'的礼物'+',请尽量打包投喂'
						await self.sendDanmu(res)
						return
				# if GiftName in gifts or ('辣条' == GiftName and GiftNum >= 20) or ( GiftName in gifts_low and GiftNum >= 8):
				# #elif '辣条' not in GiftName or GiftNum >= 10:
				# 	res='谢谢 ' + GiftUser + ' 送的 ' + GiftName + 'x' + str(GiftNum)
				# else:
				# 	return
				# await self.sendDanmu(res)
			except Exception as e:
				print(355,e,GiftUser)
			return

		if cmd == 'WELCOME_GUARD' :
			try:
				commentUser = dic['data']['username']
				t=datetime.datetime.now()
				time_hour=t.hour
				tt=t.strftime('%H:%M')
				res=""
				if  time_hour <= 6 :
					res = commentUser + ',半夜好.北京时间:'+tt
				elif time_hour <= 12 :
					res = commentUser + ",早上好.北京时间:"+tt
				elif time_hour <= 18 :
					res = commentUser + ",下午好.北京时间:"+tt
				else:
					res = commentUser + ",晚上好.北京时间:"+tt

				await self.sendDanmu(res)
			except Exception as e:
				print(372,e)
				pass			
		if cmd == 'WELCOME' :
			commentUser = dic['data']['uname']
			try:
				await self.sendDanmu('欢迎 ' + commentUser + ' 进入房间。。。。')
			except Exception as e:
				print(360,e)
				pass
			return
	async def extended_func(self,commentText):
		pass
##---------点歌机加自动回复机器人---------------------------------------
class MusicClient(DanmuJi):
	"""docstring for MusicClient"""
	def __init__(self,username,roomid = 2570641,useDanmuType = "ws"):
		super(MusicClient,self).__init__(username=username,roomid=roomid,useDanmuType=useDanmuType)
		# self.arg = arg

	async def extended_func(self,commentText):
		if "点歌" == commentText[0:2]:
			try:
				song=commentText.replace('点歌','')
				if  song:
					os.chdir('../music')
					status=os.popen("netease-dl --quiet --lyric song --name '%s'"%(song)).read()
					await self.sendDanmu(status)
					if "下载" in status:
						os.system("ps -ef|grep ffmpeg|grep bgm|awk '{print$2}'|xargs kill -9")
			except Exception as e:
				print(463,e)
			return
		if "切歌" == commentText:
			try:
				os.system('killall ffmpeg')
			except Exception as e:
				print(468,e)
			return		
class DanmujiManager(BaseClientManager):
	def __init__(self,info = [],useDanmuType = 'ws'):
		self.info = info 
		self.useDanmuType = useDanmuType

	def getTasks(self):
		tasks = []	
		for each in self.info:
			task = DanmuJi(username = each['username'],roomid = each['roomid'],useDanmuType = self.useDanmuType)
			tasks += [ task.start(),task.heartBeat() ]
		return tasks
class MusicClientManager(DanmujiManager):
	def getTasks(self):
		tasks = []	
		for each in self.info:
			task = MusicClient(username = each['username'],roomid = each['roomid'],useDanmuType = self.useDanmuType)
			tasks += [ task.start(),task.heartBeat() ]
		return tasks

##------单个房间风暴客户端-----------------------------------------
class BeatStormClient(BaseWebSocketDanmuClient):

	def __init__(self,cookies_list = [],record = False,roomid = 2570641,useDanmuType = "ws"):
		super(BeatStormClient,self).__init__(roomid=roomid,useDanmuType = useDanmuType)
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
					status = await self.sendDanmu(content)
					print(send_uname+'say:'+content)
					if self.record:
						addFengbao(fengbaoId,self.roomid,send_uid,send_uname,content,status)
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
			status = False
			for cookies in self.cookies_list:
				async with  aiohttp.ClientSession(cookies=cookies) as s:
					async with  s.post(send_url,headers=headers,data=data) as res:
						await res.text()
						r = await res.text()
						r=json.loads(r)
						print(r)
						##判断是否抢风暴成功
						if r.get('msg','')=="OK" and r.get('message','')=="OK":
							status = True						
		except Exception as e:
			print("发送弹幕失败!",e)
		
		return status

##------批量房间风暴客户端管理器-----------------------------------------
class BeatStormClientManager(BaseClientManager):
	"""docstring for BeatStormClientManager"""
	def __init__(self,cookies_list = [],record = False,roomList = [2570641],useDanmuType = "ws"):
		super(BeatStormClientManager,self).__init__(roomList = roomList,useDanmuType = useDanmuType)
		self.cookies_list = cookies_list
		self.record = record

	def getTasks(self):
		tasks = []	
		for each in self.roomList:
			task = BeatStormClient(cookies_list = self.cookies_list,record = self.record,roomid = each,useDanmuType = self.useDanmuType)
			tasks += [ task.start(),task.heartBeat() ]
		return tasks

		


if __name__ == "__main__":
	
# ##-------批量房间弹幕监控-----------------------------------------	
# 	roomList = [ 1273106,80397,1313 ]#771423,
# 	danmuClientManager = BaseClientManager(roomList = roomList)	
# 	danmuClientManager.start()


##---------单房间自动回复弹幕姬--------------------------------------
	#登录B站获取cookies	
	info = [{'username':'979365217@qq.com','roomid':2570641}]	
	Manager = MusicClientManager(info = info,useDanmuType = 'ws')
	Manager.start()


'''	
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
	BSCM = BeatStormClientManager(cookies_list = cookies_list,record = True,roomList = roomList,useDanmuType = "ws")
	BSCM.start()

'''