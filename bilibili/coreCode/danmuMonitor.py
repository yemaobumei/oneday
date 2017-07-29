#!/usr/bin/python3
#encoding=utf-8

from wssAsynDanmu import *

if __name__ == "__main__":
	
##-------批量房间弹幕监控-----------------------------------------	

	roomList =  [ 1273106,80397,1313,100798,771423,193520]
	Manager = BaseClientManager(roomList = roomList,useDanmuType = "wss")	
	Manager.start()