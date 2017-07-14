#!/usr/bin/python3
#coding=utf-8

import requests
import os,sys
import time
sys.path.append("../")
from helper import config
from helper.api import MyError
#获取最新热门直播房间号

class GetTopUpRoomId():
	def __init__(self, startPage,endPage):
		self.startPage = startPage
		self.endPage = endPage
		self.s = requests.Session()
		# self.s.proxies = config.proxies
		self.s.keep_alive = False
		self.s.trust_env = False
		self.room = []
	def saveRoom(self):
		f=open('room.py','w')
		f.write('room=%s'%(self.room))
		f.close()
	def start(self):
		room = []
		for i in range(self.startPage,self.endPage):
			j=0
			while True:
				j += 1
				if j > 40:
					raise MyError('获取最新直播房间号失败')	
				try:
					r=self.s.get('http://api.live.bilibili.com/area/liveList?area=all&order=online&page=%s'%(i),timeout=5)
					if r.status_code==200:
						data=r.json()['data']
						for each_room in data:
							room.append(each_room['roomid'])
						break
					else:
						raise MyError("获取直播信息失败第%s次,http错误号:%s"%(j,r.status_code))
				except Exception as e:
					print("getUpTop.py:37",e)
					#查询代理ip地址
					#http://www.daxiangdaili.com/api?tid=559329887212274
					#更换代理ip地址
					try:				
						response=requests.get("http://vtp.daxiangdaili.com/ip/?tid=559329887212274&num=1&protocol=http&operator=1&delay=1&filter=on",timeout=5)
						ip=response.text
						if response.status_code == 200:
							self.s.proxies['http']=ip
							self.s.proxies['https']=ip
							#print(ip)
							f=open('../helper/config.py','w')
							f.write('proxies=%s'%(self.s.proxies))
							f.close()
						else:
							raise MyError("代理ip失败,http_code:%s"%(response.status_code))
					except Exception as e:
						print("getUpTop.py:59",e)
				finally:
					time.sleep(1)#休息一下，防止访问频率太高
		room=list(set(room))
		self.room = room
		self.saveRoom()
		return room



if __name__ == '__main__':
	room=GetTopUpRoomId(0,7).start()
	print("共有房间数字:",len(room))
