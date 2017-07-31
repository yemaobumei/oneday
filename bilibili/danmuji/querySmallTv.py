import sys
sys.path.append("../")

from helper.sql import *
# from datetime import datetime,timedelta
# addSmallTv(1222,1,1)
# addFengbao(123,123,123,'yefan','风暴',True)
session = DBSession()
for instance in session.query(SmallTv).order_by(SmallTv.id):#filter_by(fansnum=0): 
	print(instance.tv_id,instance.roomid,instance.date)

session.close()