import sys
sys.path.append("../")

from helper.sql import *
# from datetime import datetime,timedelta
# addSmallTv(1222,1,1)
# addFengbao(123,123,123,'yefan','风暴',True)
session = DBSession()
for instance in session.query(Fengbao).order_by(Fengbao.date):#filter_by(fansnum=0): 
	print(instance.fengbao_id,instance.realRoomid,instance.send_uname,instance.content,instance.date,instance.status)

session.close()
