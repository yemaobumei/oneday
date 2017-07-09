#!/usr/bin/python3
#coding=utf-8
############################################################
#
#	bilibli api
#
############################################################
import os,sys
sys.path.append("../")
import requests
import requests.utils
import pickle
import json
import rsa
import binascii
from bs4 import BeautifulSoup
import urllib
import time
import asyncio
from helper import config
headers = {
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
	'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
}
# headers = {
# 	'Accept-Language': 'zh-CN,zh;q=0.8',
# 	'Accept-Encoding': 'gzip',
# 	'Referer': 'http://www.bilibili.com/',
# 	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:45.0) Gecko/20100101 Firefox/45.0'
# }
class MyError(Exception):
	"""docstring for ClassName"""
	def __init__(self, value):
		super(Exception, self).__init__()
		self.value = value
	def __str__(self):
		return repr(self.value)
		
def loop(func):
	
	async def wrap(self):
		while True:			
			startTime=time.time()
			func(self)
			endTime=time.time()
			await asyncio.sleep(24*60*60-endTime+startTime)
	return wrap

class Client():
	def __init__(self,username,password):
		self.session = requests.Session()
		self.session.headers = headers
		self.session.proxies = config.proxies
		self.userdata={}
		self.isLogin=False
		self.cookies={}
		self.username=username
		self.password=password
		self.nickname=""

	#密码执行加密
	def _encrypt(self):
		#获取加密的token
		response = self.session.get('http://passport.bilibili.com/login?act=getkey')
		token = json.loads(response.content.decode('utf-8'))
		password = str(token['hash'] + self.password).encode('utf-8')
		pub_key = token['key']
		pub_key = rsa.PublicKey.load_pkcs1_openssl_pem(pub_key)
		message = rsa.encrypt(password, pub_key)
		message = binascii.b2a_base64(message)
		return message

	def load_cookies(self):
		#读取cookies文件
		cookies_file = os.path.join(os.path.dirname(__file__), self.username + ".cookies")		
		with open(cookies_file, 'rb') as f:
			self.cookies=pickle.load(f)
			self.session.cookies = requests.utils.cookiejar_from_dict(self.cookies)



	def save_cookies(self):
		#存储cookies文件
		cookies_file = os.path.join(os.path.dirname(__file__), self.username + ".cookies")
		with open(cookies_file, 'wb') as f:
			cookies_dic = requests.utils.dict_from_cookiejar(self.session.cookies)
			pickle.dump(cookies_dic, f)


	#普通网页接口登陆，需要验证码
	def login(self):
		print(self.username+' 进入登录程序.')
		root_path = os.path.dirname(os.path.realpath(sys.argv[0]))
		#访问登陆页面
		response = self.session.get('https://passport.bilibili.com/login')
		#请求验证码图片
		response = self.session.get('https://passport.bilibili.com/captcha')
		#保存验证码
		captcha_file = os.path.join(root_path, "captcha.png")
		f = open(captcha_file,'wb')
		f.write(response.content)
		f.close()
		#密码加密
		password = self._encrypt()
		captcha_code = input(self.username+" 请输入图片上的验证码：")
		#请求登陆
		preload = {
			'act': 'login',
			'gourl': '',
			'keeptime': '2592000',
			'userid': self.username,
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
			#保存cookies			
			self.save_cookies()

			#提示语
			print('欢迎您:', self.username)
			print('登陆状态已储存，您现在可以使用其他功能脚本啦')
			return True
			
	#使用cookies登陆
	def cookies_login(self):
		#读取cookies文件
		cookies_file = os.path.join(os.path.dirname(__file__), self.username + ".cookies")
		if not os.path.exists(cookies_file):
			print(self.username + '.cookies不存在，请登录')
			return False
		self.load_cookies()
		if not self.get_account_info():
			print(self.username + '.cookies失效，请登录')
			return None,None
		print('欢迎您:', self.username)
		self.isLogin=True
		return self.cookies,self.nickname #dict{}
	@loop
	def do_sign(self):
		self.load_cookies()
		log=open('./sign.log','a')
		url = "http://live.bilibili.com/sign/doSign"
		r = self.session.get(url)
		data = json.loads(r.text)
		print(data['msg'])
		log.write(time.strftime("%Y-%m-%d ", time.localtime())+data['msg']+'\n')
		log.close()

	#获取个人信息
	def get_account_info(self):
		response = self.session.get('https://account.bilibili.com/home/userInfo',timeout=5)
		data = json.loads(response.content.decode('utf-8'))
		if data['status'] == True:
			self.userdata = data['data']
			self.nickname=data['data']['uname']
			self.isLogin=True
			return True
		return False

	def sendDanmu(self,roomid,msg):
		send_url="http://live.bilibili.com/msg/send"
		method="POST"
		data={
			'color':'16772431',
			'fontsize':25,
			'mode':1,
			'msg':msg,
			'rnd':'1493972251',
			'roomid':roomid		
		}
		res = self.session.post(send_url,data=data)
		if res.status_code==200:
			print('弹幕发送成功')


	#获取个人通知消息个数
	def get_notify_count(self):
		#CaptchaKey
		response = self.session.get('http://www.bilibili.com/plus/widget/ajaxGetCaptchaKey.php?js')
		captcha = response.text.split('\"')[1]
		response = self.session.get('http://message.bilibili.com/api/notify/query.notify.count.do?captcha=' + captcha)

	#抢沙发
	def do_reply(self, avid, content):
		print("开始抢沙发：", content)
		preload = {
			"jsonp":"jsonp",
			"message":content,
			"type":1, 
			"plat":1,
			"oid":avid
		}
		preload = urllib.parse.urlencode(preload) 
		response = self.session.post("http://api.bilibili.com/x/reply/add", data=preload)
		print(response.text)

	#获取番剧详情
	def get_bangumi_detail(self, bangumi_id):
		response = self.session.post("http://bangumi.bilibili.com/jsonp/seasoninfo/{}.ver".format(bangumi_id))
		data = json.loads(response.content.decode('utf-8'))
		try:
			if data['code'] == 0:
				return data['result']
		except Exception as e:
			print('error', e)


		