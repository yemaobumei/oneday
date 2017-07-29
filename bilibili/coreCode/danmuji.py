#!/usr/bin/python3
#encoding=utf-8

from wssAsynDanmu import *
if __name__ == '__main__':
	
#---------批量房间自动回复弹幕姬--------------------------------------
	info = [		
				{'username':'1723506002@qq.com','roomid':'4416185'},
			]	
	Manager = DanmujiManager(info=info,useDanmuType='wss')
	Manager.start()

##---------批量房间点歌机带弹幕姬功能--------------------------------
	# info = [{'username':'979365217@qq.com','roomid':2570641},]	
	# Manager = MusicClientManager(info = info,useDanmuType = 'ws')
	# Manager.start()