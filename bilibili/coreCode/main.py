#!/usr/bin/python3
#encoding=utf-8

from wssAsynDanmu import *
import room



if __name__ == "__main__":
	
##-------批量房间弹幕监控-----------------------------------------	
	import room
	roomList =  [ 1273106,80397,1313,100798,771423]
	Manager = BaseClientManager(roomList = roomList)	
	Manager.start()


##---------批量房间自动回复弹幕姬--------------------------------------
	# info = [{'username':'979365217@qq.com','roomid':2570641},]	
	# Manager = DanmujiManager(info=info,useDanmuType='wss')
	# Manager.start()

##---------批量房间点歌机带弹幕姬功能--------------------------------
	# info = [{'username':'979365217@qq.com','roomid':2570641},]	
	# Manager = MusicClientManager(info = info,useDanmuType = 'ws')
	# Manager.start()


#---------批量账号挂机抢福利----------------------------------------
	# info = [{'username':'979365217@qq.com','roomid':2570641},]	#不写房间号可以，默认2570641

	# info = [
	# 	{'username':'13126772351'},
	# 	{'username':'979365217@qq.com'},
	# 	{'username':'13375190907'},
	# 	{'username':'13390776820'},
	# 	{'username':'15675178724'},
	# 	{'username':'15130169870'},
	# 	{'username':'1723506002@qq.com'},
	# ]
	# Manager = GuaJiBaoClientManager(info=info,useDanmuType='wss')
	# Manager.start()


# ##--------批量房间风暴监控-----------------------------------------
# 	import room771423
# 	from helper.api import Client,MyError
# 	from getTopUp import GetTopUpRoomId
	
# 	#登录B站获取cookies	
# 	info = [
# 	#	{'username':'13126772351','password':'ye06021123','roomid':4416185},
# 		{'username':'979365217@qq.com','password':'ye06021123','roomid':2570641},
# 	#	{'username':'13375190907','password':'licca0907','roomid':2570641},
# 	#	{'username':'13390776820','password':'wsglr3636...','roomid':2570641},
# 	#	{'username':'15675178724','password':'zero082570X','roomid':4416185},
# 	#	{'username':'15130169870','password':'30169870.','roomid':4416185}
# 	]


# 	#获取最新热门直播房间号
# 	try:
# 		roomList = room.room
# 		if len(roomList) == 0:
# 			raise MyError("最新热门房间号为空!")
# 	except Exception as e:
# 		roomList = GetTopUpRoomId(0,7).start()
# 	print(len(roomList))

# 	#开启节奏风暴管理器
# 	BSCM = BeatStormClientManager(info = info,record = True,roomList = roomList,useDanmuType = "ws")
# 	BSCM.start()
