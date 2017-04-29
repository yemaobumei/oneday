#coding=utf-8

import requests
import json
import time

def loop(func):
	
	def wrap(headers):
		for i in range(1000):			
			startTime=time.time()
			func(headers)
			endTime=time.time()
			time.sleep(24*60*60-endTime+startTime)
	return wrap	

def read_cookie(cookiepath):
	with open(cookiepath, 'r') as fid:
		cookies = fid.readlines()
	return cookies
@loop
def do_sign(headers):
	log=open('./log.txt','a')
	url = "http://live.bilibili.com/sign/doSign"
	r = requests.get(url,headers=headers)
	data = json.loads(r.text)
	print data['code']
	if data['code']!=-500:
		log.write(time.strftime("%Y-%m-%d ", time.localtime())+data['code']+'\n')
	else:
		log.write(time.strftime("%Y-%m-%d ", time.localtime())+'success'+'\n')
	log.close()

if __name__=='__main__':
	cookies = read_cookie('./bilicookies.txt')[0]
	headers = {
	    'accept-encoding': 'gzip, deflate, sdch',
	    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.16 Safari/537.36',
	    'authority': 'live.bilibili.com',
	    'cookie': cookies,
	}
	do_sign(headers)
