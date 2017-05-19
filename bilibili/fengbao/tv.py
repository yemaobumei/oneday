from sql import *
# addSmallTv(1222,1,1)
session = DBSession()
for instance in session.query(Fengbao).order_by(Fengbao.date):#filter_by(fansnum=0): 
	print(instance.realRoomid,instance.send_uname,instance.date)
	#session.delete(instance)
session.commit()
session.close()
