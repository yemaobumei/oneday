from sql import *
# addSmallTv(1222,1,1)
session = DBSession()
for instance in session.query(SmallTv).all():#filter_by(fansnum=0): 
	print(instance.tv_id,instance.roomid)
	session.delete(instance)
session.commit()
session.close()
