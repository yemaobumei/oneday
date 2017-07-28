import sys
sys.path.append("../")
from helper.sql import *
from sqlalchemy import func 

session = DBSession()
fengbaoList = session.query(func.count(Fengbao.realRoomid),Fengbao.realRoomid).group_by(Fengbao.realRoomid).all() 
# [(1, 1017), (2, 5067), (1, 5123)]
length = len(fengbaoList)
for i in range(length-1):
	for j in range(length-1):
		if fengbaoList[j][0]<fengbaoList[j+1][0]:
			temp = fengbaoList[j]
			fengbaoList[j] = fengbaoList[j+1]
			fengbaoList[j+1] = temp
print(fengbaoList)