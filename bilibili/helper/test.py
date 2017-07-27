#!/usr/bin/python3
#coding=utf-8
import requests
from api import Client
import time

room_id = "2570641"
headers = {
    'user-agent': 'Mozilla/5.0 BiliDroid/4.34.0 (bbcallen@gmail.com)',
    'referer': 'https://live.bilibili.com/'
  }
headers['content-type'] = 'application/x-www-form-urlencoded; charset=UTF-8'

headers={
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
			'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
			'referer': 'https://live.bilibili.com/157901'
		}
referer_header = 'http://live.bilibili.com/' + room_id
def heart(requester):
	'''
	heartbeat
	'''
	heart_url = 'http://live.bilibili.com/User/userOnlineHeart'
	res = requester.post(heart_url, headers=headers).json()
	return res

username="979365217@qq.com"
password="ye06021123"
LoginClient=Client(username,password)
cookies,nickname=LoginClient.cookies_login()
s = requests.Session()
s.trust_env=False
s.cookies=requests.utils.cookiejar_from_dict(cookies, cookiejar=None, overwrite=True)
for i in range(10):
	r=heart(s)
	print(r)
	time.sleep(300)

# 157901
