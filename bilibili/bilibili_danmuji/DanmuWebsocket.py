#!/usr/bin/python3
#coding=utf-8

import asyncio
import aiohttp
import xml.dom.minidom
import random
import json
from struct import *
import config
import re

#api.py
import os,sys
import requests
import requests.utils
import pickle
import json
import rsa
import binascii
from bs4 import BeautifulSoup


#helper
import difflib
import math
import datetime
import random
import logging

headers={
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
			'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
		}

logging.basicConfig(level=logging.DEBUG,
		format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
		datefmt='%a, %d %b %Y %H:%M:%S',
		filename='bilibili.log',
		filemode='w')
class DanmuWebsocket():
	def __init__(self,cookies):
		self._CIDInfoUrl = 'http://live.bilibili.com/api/player?id=cid:'
		self._roomId = 0
		self._ChatPort = 788
		self._protocolversion = 1
		self._reader = 0
		self._writer = 0
		self.connected = False
		self._UserCount = 0
		self._ChatHost = 'livecmt-1.bilibili.com'

		self._roomId = "1273106" #"2570641"  #"1619217"
		self._roomId = int(self._roomId)



		self.cookies=cookies
#---辅助弹幕部分--------------------------------------------------------------------------
		self.send_danmu_num=0
		self.gift_dic={}
		self.gift_num=0

		self.recevie_danmu_num=0
		self.database={
		'背景音乐':'网易云ID:喵咭喵呜QAQ,关注有歌单',
		'求bgm网易云':'网易云ID:喵咭喵呜QAQ,关注有歌单',
		'玩什么段位英雄':'主播钻石水平，日常AD。想看什么英雄可以跟主播说',
		 '下路炸了超鬼':'主播加油，胜利在望，决不动摇',
		 'gay玩弹幕姬':'放马过来调戏我',
		 '主播小姐姐真漂亮美':'喵咭和往常一样漂亮',
		 '今晚日常修仙吗':'不要修仙哟，对身体不好呢',
		 '唱歌好听':'主播唱歌贼好听',
		 '废话大佬在哪呢':'废话被麻麻gank了',
		 '夜猫大佬不在了去哪了':'不要趁我不在就gay我，我与喵咭共存亡',
		 'Bb克拉领个勋章':'送个b克拉领个勋章,周末一起水友赛',
		 '怎么喵咭戴勋章':'pc端右下角发送弹幕框下有个"勋"字,手机端直播中心我的勋章',
		 '直播群粉丝群':'粉丝QQ群:339145940',	
	}

		self.setTimeDanmu=[ '大家多和主播交流,也可以@夜猫和我聊天哟,我可是百事通呢',
							'喜欢主播右上角点点关注,送点小礼物帮主播升升级',
							'主播人美声甜游戏打的贼6,喜欢的朋友点点关注,加加粉丝群',
							'喜欢主播的大佬可以上波船,船上风景别有一番滋味呢',
							'点关注不迷路，主播带你上高速',
							'想和主播一起玩游戏吗，还不快上船'
						]

	async def sendDanmu(self,msg):
		send_url="http://live.bilibili.com/msg/send"
		method="POST"
		msg=msg.strip()
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
			'roomid':self._roomId     
		}
		async with  aiohttp.ClientSession(cookies=self.cookies) as s:
			async with  s.post(send_url,headers=headers,data=data) as res:
				await res.text()
				if res.status==200:
					self.send_danmu_num+=1
					print(108,msg,self.send_danmu_num)

	async def send_long_danmu(self,msg):
		length=len(msg)
		c=math.ceil(length/30.0)
		for i in range(c):
			await self.sendDanmu(msg[i*30:(i+1)*30])
					
	async def robot(self,username,msg):
		s=['夜猫','弹幕姬']#'主播','喵咭',
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
			#print(temp_ratio,temp_key)

		except Exception as e:
			print(145,e)
	
		if (temp_ratio > 0.49 and len(msg) <= 10) or (temp_ratio > 0.34 and len(msg) > 10) or (temp_ratio >0.2 and len(msg)>20) :
			await self.sendDanmu(self.database[temp_key])
			return
		else:
			contains=[each for each in s if each in msg]
			if any(contains):
				for con in contains:
					msg=msg.replace(con,' ')
				data['info'] = msg
				r=requests.post(url,data=data)
				response=json.loads(r.content.decode('utf-8'))['text']
				#print(152,response)
				await self.sendDanmu(response+'@'+username)

		return












	# def connection_info(self):
	# 	r=self.session.get('http://live.bilibili.com/' + str(self._roomId))
	# 	html=r.content.decode('utf8')
	# 	m = re.findall(r'ROOMID\s=\s(\d+)', html)
	# 	ROOMID = m[0]
	# 	self._roomId = int(ROOMID)
	# 	r2=self.session.get(self._CIDInfoUrl + ROOMID)
	# 	xml_string = '<root>' + r2.content.decode('utf8') + '</root>'
	# 	dom = xml.dom.minidom.parseString(xml_string)
	# 	root = dom.documentElement
	# 	server = root.getElementsByTagName('server')
	# 	self._ChatHost = server[0].firstChild.data

	async def connectServer(self):
		print ('正在进入房间。。。。。')
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
		print ('链接弹幕中。。。。。')
		if (await self.SendJoinChannel(self._roomId) == True):
			self.connected = True
			print ('进入房间成功。。。。。')
			print ('链接弹幕成功。。。。。')
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
					print ('房间人数为 %s' % num3)
					self._UserCount = num3
					continue
				elif num==3 or num==4:
					tmp = await self._reader.read(num2)
					# strbytes, = unpack('!s', tmp)
					try: # 为什么还会出现 utf-8 decode error??????
						messages = tmp.decode('utf-8')
					except:
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
		except Exception as e: # 有些情况会 jsondecode 失败，未细究，可能平台导致
			print(276,e)
			return
		cmd = dic['cmd']
		if cmd == 'LIVE':
			print ('直播开始。。。')
			return
		if cmd == 'PREPARING':
			print ('房主准备中。。。')
			return
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
			if "喵咭大佬弹幕姬专用の夜猫" in commentUser:
				return 
			if isAdmin:
				commentUser = '管理员 ' + commentUser
			if isVIP:
				commentUser = 'VIP ' + commentUser
			try:
				print (311,commentUser + ' say: ' + commentText)
				await self.robot(commentUser,commentText)
			except Exception as e:
				print(314,e)
				pass
			return
		if cmd == 'SEND_GIFT' and config.TURN_GIFT == 1:
			#累计多次礼物后，情况礼物清单栏,{'a':3,'b':5}
			self.gift_num+=1
			if self.gift_num % 40 == 0:
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
			print (332,GiftName,GiftNum)

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
				elif GiftName in gifts or ('辣条' == GiftName and GiftNum >= 20) or ( GiftName in gifts_low and GiftNum >= 8):
				#elif '辣条' not in GiftName or GiftNum >= 10:
					res='谢谢 ' + GiftUser + ' 送的 ' + GiftName + 'x' + str(GiftNum)
				else:
					return
				await self.sendDanmu(res)
			except Exception as e:
				print(355,e,GiftUser)
				pass
			return
		if cmd == 'WELCOME' and config.TURN_WELCOME == 1:
			commentUser = dic['data']['uname']
			try:
				print (357,'欢迎 ' + commentUser + ' 进入房间。。。。')
				await self.sendDanmu('欢迎 ' + commentUser + ' 进入房间。。。。')
			except Exception as e:
				print(360,e)
				pass
			return
		if cmd == 'WELCOME_GUARD' and config.TURN_WELCOME == 1:
			try:
				commentUser = dic['data']['username']
				time_hour=datetime.datetime.now().hour
				res=""
				if  time_hour <= 6 :
					res = commentUser + ',半夜好'
				elif time_hour <= 12 :
					res = commentUser + ",早上好"
				elif time_hour <= 18 :
					res = commentUser + ",下午好"
				else:
					res = commentUser + ",晚上好"

				await self.sendDanmu(res)
			except Exception as e:
				print(372,e)
				pass
			return
		return
