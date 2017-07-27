#!/usr/bin/python3
#encoding=utf-8
import websocket  #websocket-client包
import _thread,threading
import time
import random
import json
import re
import requests
from struct import *



class WebSocketDanmu():

	def __init__(self, roomid = 2570641):
		self.roomid = int(roomid)
	#获取主播真实房间号
	def connection_info(self):
		s = requests.session()
		s.trust_env = False
		r = s.get('http://live.bilibili.com/' + str(self.roomid))
		html = r.text
		m = re.findall(r'ROOMID\s=\s(\d+)', html)
		self.roomid = int(m[0])
	#"服务器推送数据"
	def push(self, ws, data = b'', type = 7):
		data = (pack('>i', len(data) + 16) + b'\x00\x10\x00\x01' + pack('>i', type) + pack('>i', 1) + data)
		ws.send(data)
	#弹幕池心跳包	
	def heartbeat(self,ws):
		while True:
			self.push(ws,data=b'',type=2)
			time.sleep(30)
	def on_message(self,ws, message):
		dic = {}
		try:
			for msg in re.findall(b'\x00({[^\x00]*})', message):
				msg = msg.decode('utf-8','ignore')
				dic = json.loads(msg)
		except Exception as e:
			print("解码失败:",e)
		else:
			cmd = dic.get('cmd','')

			if cmd == 'DANMU_MSG':					
				commentText = dic['info'][1]
				commentUser = dic['info'][2][1]
				print (commentUser + ' say: ' + commentText)				
				return

			if cmd == 'SEND_GIFT' :
				data = dic.get('data','')
				#获取送礼信息		
				GiftName = data['giftName']
				GiftUser = data['uname']
				Giftrcost = data['rcost']
				GiftNum = data['num']
				uid = data['uid']
				msg = "%s 赠送 %sx%s"%(GiftUser,GiftName,GiftNum)
				print(msg)
				return
		

	def on_error(self, ws, error):
		print(error)

	def on_close(self, ws):
		print("### closed ###")

	def on_open(self, ws):
		self.connection_info()
		#发送弹幕池连接验证信息
		data = json.dumps({
			'roomid': self.roomid,
			'uid': int(1e14 + 2e14 * random.random()),
			}, separators=(',', ':')).encode('ascii')
		self.push(ws, data = data)
		#将弹幕池心跳包加入另一个线程运行
		heart = threading.Thread(target = self.heartbeat, args = (ws,))
		heart.setDaemon(True)
		heart.start()
	def start(self):
		url = "ws://broadcastlv.chat.bilibili.com:2244/sub"	
		ws = websocket.WebSocketApp(url,
								  on_message = self.on_message,
								  on_error = self.on_error,
								  on_close = self.on_close)
		ws.on_open = self.on_open
		ws.run_forever()
if __name__ == "__main__":
	# websocket.enableTrace(True)
	WebSocketDanmu('447').start()
