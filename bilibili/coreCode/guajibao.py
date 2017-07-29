#!/usr/bin/python3
#encoding=utf-8

from wssAsynDanmu import *

if __name__ == "__main__":
##---------批量账号挂机抢福利----------------------------------------
	
	info = [
		# {'username':'13126772351'},
		# {'username':'979365217@qq.com'},
		# {'username':'13375190907'},
		# {'username':'13390776820'},
		# {'username':'15675178724'},
		# {'username':'15130169870'},
		{'username':'1723506002@qq.com'},
	]
	Manager = GuaJiBaoClientManager(info=info,useDanmuType='wss')
	Manager.start()