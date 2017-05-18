from sql import *
# addSmallTv(1222,1,1)
addFengbao(1111,212,'xx')
session = DBSession()
for instance in session.query(User).filter_by(realRoomid=1111).all():#filter_by(fansnum=0): 
	print(instance.realRoomid,instance.fengbaoNum)
	#session.delete(instance)
session.commit()
session.close()
