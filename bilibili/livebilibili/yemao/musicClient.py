import sys
sys.path.append('../../')
from coreCode.wssAsynDanmu import MusicClientManager

if __name__ == '__main__':
	info = [{'username':'13126772351','roomid':2570641}]	
	Manager = MusicClientManager(info = info,useDanmuType = 'ws')
	Manager.start()