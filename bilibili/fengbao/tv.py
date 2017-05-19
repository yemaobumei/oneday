from sql import *
# addSmallTv(1222,1,1)
session = DBSession()
for instance in session.query(Fengbao).filter_by(realRoomid=1589452).all():#filter_by(fansnum=0): 
	print(instance.realRoomid,instance.send_uname)
	#session.delete(instance)
session.commit()
session.close()
