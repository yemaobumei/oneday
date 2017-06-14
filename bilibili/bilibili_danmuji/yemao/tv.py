from sql import *
#addSmallTv('1222',1,1)
realRoomid='1222'
session = DBSession()
for instance in session.query(SmallTv).order_by(SmallTv.date):#filter_by(fansnum=0): 
	print(instance.tv_id,instance.realRoomid,instance.date)
	#session.delete(instance)

session.commit()
session.close()
