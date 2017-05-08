#!/usr/bin/python3
#coding=utf-8

import requests
import requests.utils
import json,pickle
import time
import sys,os

def loop(func):
	
	def wrap(self):
		for i in range(1000):			
			startTime=time.time()
			func(self)
			endTime=time.time()
			time.sleep(24*60*60-endTime+startTime)
	return wrap

class DoSign():
	def __init__(self,username):
		self.session=requests.Session()
		self.session.headers={
		    'accept-encoding': 'gzip, deflate, sdch',
		    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.16 Safari/537.36',
		    'authority': 'live.bilibili.com',
		}
		self.username=username

	def load_cookies(self):
		root_path = os.path.dirname(os.path.realpath(sys.argv[0]))

		#读取cookies文件
		cookies_file = os.path.join(root_path, self.username + ".cookies")
		if not os.path.exists(cookies_file):
			print(self.username + '.cookies不存在，请登录')
			sys.exit()
		with open(cookies_file, 'rb') as f:
			cookies=requests.utils.cookiejar_from_dict(pickle.load(f))
			self.session.cookies=cookies
			print('cookies载入成功')
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
if __name__=='__main__':
	username='13126772351'
	sign=DoSign(username)
	sign.do_sign()
