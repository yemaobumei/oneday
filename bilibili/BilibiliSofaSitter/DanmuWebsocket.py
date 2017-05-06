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
import urllib

#compare str
import difflib

#helper
import math

class DanmuWebsocket():
	def __init__(self):
		self._CIDInfoUrl = 'http://live.bilibili.com/api/player?id=cid:'
		self._roomId = 0
		self._ChatPort = 788
		self._protocolversion = 1
		self._reader = 0
		self._writer = 0
		self.connected = False
		self._UserCount = 0
		self._ChatHost = 'livecmt-1.bilibili.com'

		self._roomId = "1273106"  #"1619217"
		self._roomId = int(self._roomId)


#---login.py部分-----------------------------------------------------------------------
		self.session = requests.Session()
		self.session.headers = {
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
			'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
		}
		self.userdata = ''
		self.isLogin=False
#---辅助弹幕部分--------------------------------------------------------------------------
		self.danmu_num=0
		self.gift_dic={}
		self.gift_num=0
		self.gift_inc=20
		self.database={
		'背景音乐':'网易云ID:喵咭喵呜QAQ,关注有歌单',
		'求bgm网易云':'网易云ID:喵咭喵呜QAQ,关注有歌单',
		'66666':'主播这么厉害不点拨关注吗',
		'做鸡巴儿':'请大家注意弹幕礼仪',
		'真的菜水':'这只是发挥失常，大家看久点就知道了',
		'玩什么段位英雄':'主播钻石水平，日常AD。想看什么英雄可以跟主播说',
		 '下路炸了超鬼':'主播加油，胜利在望，决不动摇',
		 'gay玩弹幕姬':'不要调戏我，会坏的',
		 '小姐姐漂亮':'喵咭和往常一样漂亮',
		 '主播真漂亮':'喵咭和往常一样漂亮',
		 '日常修仙吗':'不要休闲哟，对身体不好呢',
		 '唱歌好听':'主播唱歌贼好听',
		 '废话大佬在哪呢':'废话被麻麻gank了',
		 '夜猫大佬不在了':'不要趁我不在就gay我，我与喵咭共存亡',
		 '蚂蚱':'蚂蚱好帅，好想给你生猴子',
		 'b克拉领个勋章':'送个b克拉领个勋章,周末一起水友赛',
		 '怎么戴勋章':'pc端右上角直播中心佩戴中心,手机端直播中心我的勋章',	
	}
	#密码执行加密
	def _encrypt(self, password):
		#获取加密的token
		response = self.session.get('http://passport.bilibili.com/login?act=getkey')
		token = json.loads(response.content.decode('utf-8'))
		password = str(token['hash'] + password).encode('utf-8')
		pub_key = token['key']
		pub_key = rsa.PublicKey.load_pkcs1_openssl_pem(pub_key)
		message = rsa.encrypt(password, pub_key)
		message = binascii.b2a_base64(message)
		return message

	def load_cookies(self, path):
		with open(path, 'rb') as f:
			self.session.cookies = requests.utils.cookiejar_from_dict(pickle.load(f))
			self.userdata = {}

	def save_cookies(self, path):
		with open(path, 'wb') as f:
			cookies_dic = requests.utils.dict_from_cookiejar(self.session.cookies)
			pickle.dump(cookies_dic, f)


	#普通网页接口登陆，需要验证码
	def login(self, username, password, captcha_path):
		#访问登陆页面
		response = self.session.get('https://passport.bilibili.com/login')
		#请求验证码图片
		response = self.session.get('https://passport.bilibili.com/captcha')
		#保存验证码
		f = open(captcha_path,'wb')
		f.write(response.content)
		f.close()
		#密码加密
		password = self._encrypt(password)
		captcha_code = input("请输入图片上的验证码：")
		#请求登陆
		preload = {
			'act': 'login',
			'gourl': '',
			'keeptime': '2592000',
			'userid': username,
			'pwd': password,
			'vdcode':captcha_code
		}
		response = self.session.post('https://passport.bilibili.com/login/dologin', data=preload)
		try:
			#解析返回的html，判断登陆成功与否
			soup = BeautifulSoup(response.text, "html.parser")
			center = soup.find('center').find('div')
			info = list(center.strings)[0]
			info = info.strip()
			print("登陆失败", info)
			return False
		except Exception as e:
			#登陆成功
			self.isLogin=True
			return True
			
	#使用cookies登陆
	def cookies_login(self):
		root_path = os.path.dirname(os.path.realpath(sys.argv[0]))
		#读取配置文件中的username
		config_path = os.path.join(root_path, 'username.config')
		try:
			f = open(config_path, 'r')
			config = json.load(f)
			username = config['username']
		except Exception as e:
			print("username.config文件不存在或内容错误，请重新执行一次login.py")
			sys.exit()
		finally:
			f.close()
		#读取cookies文件
		cookies_file = os.path.join(root_path, username + ".cookies")
		if not os.path.exists(cookies_file):
			print(username + '.cookies不存在，请重新执行一次login.py')
			sys.exit()
		self.load_cookies(cookies_file)
		if not self.get_account_info():
			print(username + '.cookies失效，请重新执行一次login.py')
			sys.exit()
		print('欢迎您:', self.userdata['uname'])
		self.isLogin=True
		return self.userdata['uname']

	#获取个人信息
	def get_account_info(self):
		response = self.session.get('https://account.bilibili.com/home/userInfo')
		data = json.loads(response.content.decode('utf-8'))
		try:
			if data['status'] == True:
				self.userdata = data['data']
				self.isLogin=True
				return True
		except Exception as e:
			print(e)
		return False


	def sendDanmu(self,msg):
		send_url="http://live.bilibili.com/msg/send"
		method="POST"
		if len(msg) > 38:
			self.send_long_danmu(msg)
		data={
			'color':'16772431',
			'fontsize':25,
			'mode':1,
			'msg':msg,
			'rnd':'1493972251',
			'roomid':self._roomId     
		}
		res = self.session.post(send_url,data)
		if res.status_code==200:
			self.danmu_num+=1
			print(msg,self.danmu_num)

	def send_long_danmu(self,msg):
		length=len(msg)
		c=math.ceil(length/30.0)
		for i in range(c):
			self.sendDanmu(msg[i*30:(i+1)*30-1])
					
	def robot(self,username,msg):
		s=['夜猫','主播','喵咭','up','弹幕姬','小姐姐']
		danmu_liyi=['胸','奶','鸡儿','脱衣']
		data={'info':msg,'key':'a85845213d8f41fc9685fff9c675ec5d'}
		#data={'info':msg,'key':'fef3ad124da348419db60d502d43bcf2'}
		url="http://www.tuling123.com/openapi/api"
		temp_ratio = 0
		temp_key=""
		try:
			if any([1 for i in danmu_liyi if i in msg]):
				self.sendDanmu('请大家注意弹幕礼仪')
				return
			if '晚安' in msg :				
				if '晚安'!= msg and '主播晚安'!= msg and '喵咭晚安' != msg:
					return
				self.sendDanmu(username+'晚安') 
				return
			if '去睡' in msg :
				self.sendDanmu(username+'晚安')
				return
			for key in self.database:
				seq = difflib.SequenceMatcher(None, msg,key)
				ratio = seq.ratio()
				if ratio > temp_ratio :
					temp_ratio = ratio
					temp_key = key
			print(temp_ratio,temp_key)

		except Exception as e:
			print(e)
	
		if (temp_ratio > 0.49 and len(msg) <= 10) or (temp_ratio > 0.34 and len(msg) > 10) or (temp_ratio >0.2 and len(msg)>20) :
			self.sendDanmu(self.database[temp_key])
			return
		else:
			contains=[each for each in s if each in msg]
			if any(contains):
				for con in contains:
					msg=msg.replace(con,' ')
				data['info'] = msg
				print(msg)
				r=requests.post(url,data=data)
				response=json.loads(r.content.decode('utf-8'))['text']
				self.sendDanmu(response+'@'+username)

		return














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
					self.parseDanMu(messages)
					continue
				elif num==5 or num==6 or num==7:
					tmp = await self._reader.read(num2)
					continue
				else:
					if num != 16:
						tmp = await self._reader.read(num2)
					else:
						continue

	def parseDanMu(self, messages):
		try:
			dic = json.loads(messages)
		except: # 有些情况会 jsondecode 失败，未细究，可能平台导致
			return
		cmd = dic['cmd']
		if cmd == 'LIVE':
			print ('直播开始。。。')
			return
		if cmd == 'PREPARING':
			print ('房主准备中。。。')
			return
		if cmd == 'DANMU_MSG':
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
				print (commentUser + ' say: ' + commentText)
				self.robot(commentUser,commentText)
			except:
				pass
			return
		if cmd == 'SEND_GIFT' and config.TURN_GIFT == 1:
			#累计多次礼物后，情况礼物清单栏,{'a':3,'b':5}
			self.gift_num+=1
			if self.gift_num%self.gift_inc==0:
				self.gift_dic={}
				self.sendDanmu('谢谢大家的关注和礼物,主播认真打游戏有些弹幕可能会漏掉,多见谅')
			#获取送礼信息		
			GiftName = dic['data']['giftName']
			GiftUser = dic['data']['uname']
			Giftrcost = dic['data']['rcost']
			GiftNum = dic['data']['num']
			print (GiftName)
			#单次送礼记录礼物清单内，连续多次后触发不弹幕'打包投喂'。
			if GiftNum==1:
				self.gift_dic[GiftUser] = self.gift_dic[GiftUser] + 1 if  GiftUser in self.gift_dic else 1
			try:
				if self.gift_dic[GiftUser] >= 5:
					self.gift_dic[GiftUser]=0
					res='谢谢'+GiftUser+'的礼物'+',请尽量打包投喂'
				elif '辣条' not in GiftName or GiftNum >= 10:
					res='谢谢' + GiftUser + ' 送的 ' + GiftName + 'x' + str(GiftNum)
				else:
					return
				#print(GiftUser + ' 送出了 ' + str(GiftNum) + ' 个 ' + GiftName)
				self.sendDanmu(res)
			except:
				pass
			return
		if cmd == 'WELCOME' and config.TURN_WELCOME == 1:
			commentUser = dic['data']['uname']
			try:
				print ('欢迎 ' + commentUser + ' 进入房间。。。。')
				self.sendDanmu('欢迎 ' + commentUser + ' 进入房间。。。。')
			except:
				pass
			return
		return
