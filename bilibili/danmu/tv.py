import sys
sys.path.append("../")

from helper.sql import *
# from datetime import datetime,timedelta
# addSmallTv(1222,1,1)
#addFengbao(123,111,'yefan')
session = DBSession()
for instance in session.query(Fengbao).order_by(Fengbao.date):#filter_by(fansnum=0): 
	print(instance.realRoomid,instance.send_uname,instance.date)
	#instance.date+=timedelta(hours=8)
session.commit()
session.close()
