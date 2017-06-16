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
import datetime,time
import random

#添加数据库操作
from sql import addSmallTv

#mp3信息获取
import eyed3

headers={
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
			'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
		}


class DanmuWebsocket():
	def __init__(self,cookies,roomid):
		self._CIDInfoUrl = 'http://live.bilibili.com/api/player?id=cid:'
		self._roomId = 0
		self._ChatPort = 788
		self._protocolversion = 1
		self._reader = 0
		self._writer = 0
		self.connected = False
		self._UserCount = 0
		self._ChatHost = 'livecmt-1.bilibili.com'

		self._roomId = roomid
		self._roomId = int(self._roomId)

		self.cookies=cookies

#---辅助弹幕部分--------------------------------------------------------------------------
		self.send_danmu_num=0
		self.gift_dic={}
		self.gift_num=0

		self.recevie_danmu_num=0
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

#------------点歌计数--------------------------------------------
		self.songNum=0

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
					#print(108,msg,self.send_danmu_num)

	async def send_long_danmu(self,msg):
		length=len(msg)
		c=math.ceil(length/30.0)
		for i in range(c):
			await self.sendDanmu(msg[i*30:(i+1)*30])
					
	async def robot(self,username,msg):
		s=['夜猫','弹幕姬','弹幕机','机器猫','主播','up']
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
				r=requests.post(url,data=data,timeout=2)
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
					#print ('房间人数为 %s' % num3)
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
			cmd = dic['cmd']
			#print(dic)
		except Exception as e: # 有些情况会 jsondecode 失败，未细究，可能平台导致
			print(276,e)
			return
		
		# if cmd == 'LIVE':
		# 	try:
		# 		#print ('直播开始。。。') #{'cmd': 'LIVE', 'roomid': 2570641}
		# 		await self.sendDanmu('喵咭晚上好,小夜猫终于等到你开播了') 
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
			# if "喵咭大佬弹幕姬专用の夜猫" in commentUser:
			# 	return 
			if isAdmin:
				commentUser = '管理员 ' + commentUser
			if isVIP:
				commentUser = 'VIP ' + commentUser
			try:
				#print (311,commentUser + ' say: ' + commentText)
				await self.robot(commentUser,commentText)
			except Exception as e:
				print(314,e)
			if "点歌" in commentText:
				try:
					song=commentText.replace('点歌','')

					if  song:
						os.chdir('../music')
						os.system("netease-dl --quiet song --name '%s'"%(song))
						# files=os.listdir('../music/')
						# for file in files:
						# 	if file.split('.')[-1]=='mp3' :
						# 		font_path="/usr/share/fonts/winFonts/msyh.ttf"
						# 		flv_name=file.split('.')[0]+'.flv'
						# 		mp3=eyed3.load(file)
						# 		seconds=mp3.info.time_secs
						# 		print(flv_name,seconds)
						# 		cmd1="ffmpeg  -loop 1 -i '0%s.jpg'   -pix_fmt yuv420p -vcodec libx264 -b:v 600k -r:v 25 -preset medium -crf 30  -vframes 250 -r 25 -t %s -s 720x576 -y SinglePictureVide.mp4"%(str(random.randint(0,6)),str(seconds))
						# 		cmd2="ffmpeg -i %s -i %s -vf drawtext=text='正在播放%s':fontfile=%s:fontsize=18:fontcolor=blue@0.8:x=w-tw-10:y=th  -b:a 256k -b:v 600k -f flv -y '%s'"%('SinglePictureVide.mp4',file,file,font_path,flv_name)
						# 		os.system(cmd1)
						# 		os.system(cmd2)
						# 		os.remove(file)
						# 		os.remove("SinglePictureVide.mp4")
						# 		f=open('./mylist.txt','w')
						# 		f.write("file '%s'\n"%(flv_name))
						# 		f.close()
						# f=open("list%s.txt"%(self.songNum),'w')
						# f.write(song)
						# f.close()
						# print(song)
						# self.songNum+=1
				except Exception as e:
					print(e)
			if "切歌" in commentText:
				try:
					print(commentText)
					os.system('killall ffmpeg')
				except Exception as e:
					print(e)
			return

		if cmd == 'SEND_GIFT' and config.TURN_GIFT == 1:
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

				res='谢谢 ' + GiftUser + ' 送的 ' + GiftName + 'x' + str(GiftNum)
				await self.sendDanmu(res)
			except Exception as e:
				print(355,e,GiftUser)
			return
		if cmd == 'WELCOME' and config.TURN_WELCOME == 1:
			commentUser = dic['data']['uname']
			try:
				#print (357,'欢迎 ' + commentUser + ' 进入房间。。。。')
				await self.sendDanmu('欢迎 ' + commentUser + ' 进入房间。。。。')
			except Exception as e:
				print(360,e)
				pass
			return
		if cmd == 'WELCOME_GUARD' and config.TURN_WELCOME == 1:
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



