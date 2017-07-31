#!/usr/bin/python3
#encoding=utf-8

from wssAsynDanmu import *


if __name__ == "__main__":
	

##--------批量房间风暴监控-----------------------------------------
	import room
	from helper.api import Client,MyError
	from getTopUp import GetTopUpRoomId
	
	#登录B站获取cookies	
	info = [
		# {'username':'13126772351'},
		{'username':'979365217@qq.com'},
		# {'username':'13375190907'},
		# {'username':'13390776820'},
		# {'username':'15675178724'},
		# {'username':'15130169870'},
		# {'username':'1723506002@qq.com'},
	]


	#获取最新热门直播房间号
	try:
		roomList = room.room
		if len(roomList) == 0:
			raise MyError("最新热门房间号为空!")
	except Exception as e:
		roomList = GetTopUpRoomId(0,7).start()
	print(len(roomList))

	#开启节奏风暴管理器
	BSCM = BeatStormClientManager(info = info,record = True,roomList = roomList,useDanmuType = "ws")
	BSCM.start()
