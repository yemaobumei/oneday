# 在Python中, 最有名的ORM框架是SQLAlchemy. 我们来看看SQLAlchemy的用法.

from sqlalchemy import Column, String,Integer, DateTime, create_engine,engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

import requests
import json
Base = declarative_base()
class User(Base):
    # 表的名字
    __tablename__ = 'user'

    # 表的结构
    id = Column(Integer,primary_key=True)
    realRoomid = Column(Integer,nullable=False,unique=True)
    uid = Column(Integer, nullable=True)
    uname = Column(String(20),nullable=True)
    roomid = Column(Integer,nullable=True)    
    fansnum = Column(Integer,nullable=True)
    areaName = Column(String(20),nullable=True)
    fengbaoNum = Column(Integer,default=0,nullable=True)
    TvNum = Column(Integer,default=0,nullable=True)
    date = Column(DateTime(timezone=True), default=func.now())

class SmallTv(Base):
	__tablename__ = 'TvRecord'
	id = Column(Integer,primary_key=True)
	tv_id = Column(Integer, nullable=False,unique=True)
	roomid = Column(Integer,nullable=False)
	real_roomid = Column(Integer,nullable=True)
	#date = Column(Date, default=datetime.today().strftime("%Y-%m-%d"), nullable=False)
	date = Column(DateTime(timezone=True), default=func.now())

class Fengbao(Base):
	__tablename__ = 'Fengbao'
	id = Column(Integer, primary_key=True)
	realRoomid = Column(Integer,nullable=False)
	send_uid = Column(Integer,nullable=True)
	send_uname = Column(String(20),nullable=True)
	date = Column(DateTime(timezone=True), default=func.now())


# 初始化数据库连接
engine = create_engine('sqlite:///ye.db', echo=False)#true控制台就会输出sql操作信息,默认Fasle
# 创建DBSession类型
DBSession = sessionmaker(bind=engine)
# create_engine用来初始化数据库连接.
# SQLAlchemy用一个字符串表示连接信息'数据库类型+数据库驱动名称://用户名:口令@机器地址:端口号/数据库名'

###建立表
Base.metadata.create_all(engine)#新建数据库表，必须使用此语句建立表结构，以后打开可以不加此语句。


def addUserList(start,end):
	room=[]
	session = DBSession()

	for i in range(start,end):
		r=requests.get('http://api.live.bilibili.com/area/liveList?area=all&order=online&page=%s'%(i))
		if r.status_code==200:
			data=json.loads(r.content.decode('utf8'))['data']
			for each_room in data:
				
				#获取主播信息
				uid=int(each_room['uid'])
				uname=each_room['uname']
				roomid=int(each_room['link'].replace('/',''))
				realRoomid=int(each_room['roomid'])
				areaName=each_room['areaName']
				online=each_room['online']
				# if online > 1000:
				# 	room.append(roomid)
				#获取主播粉丝数
				s=requests.get('http://space.bilibili.com/ajax/friend/GetFansList?mid=%s&page=1&_=1494764064486'%(uid))#mid输入uid.
				data=json.loads(s.content.decode('utf8'))['data']#可能是字典，也可能是"粉丝列表中没有值"
				fansnum=int(data['results']) if 'results' in data else 0
				print(i,uname,online)					
				queryUser=session.query(User).filter_by(realRoomid=realRoomid).first()
				if queryUser:
					#print(queryUser)
					queryUser.fansnum=fansnum
					print('exited!')
				else:	
					session.add(User(uid=uid,uname=uname,roomid=roomid,realRoomid=realRoomid,fansnum=fansnum,areaName=areaName))
	session.commit()
	session.close()
	return room

# addUserList(0,10)

def addUser(uid,uname,roomid,realRoomid,fansnum,areaName):
	session = DBSession()
	queryUser=session.query(User).filter_by(realRoomid=realRoomid).first()
	if queryUser:
		#print(queryUser)
		#queryUser.fansnum=fansnum
		#session.commit()
		print('exited!')
	else:	
		session.add(User(uid=uid,uname=uname,roomid=roomid,realRoomid=realRoomid,fansnum=fansnum,areaName=areaName))
		session.commit()
	session.close()	
# session = DBSession()
# for instance in session.query(User).order_by(User.fansnum):#filter_by(fansnum=0): 
# 	print(instance.uname,instance.uid,instance.fansnum)
# session.close()
def addSmallTv(tv_id,roomid,real_roomid):
	session = DBSession()
	try:
		session.add(SmallTv(tv_id=tv_id,roomid=roomid,real_roomid=real_roomid))
		session.commit()
		session.close()	
	except Exception as e:
		print(95,e)


def addFengbao(realRoomid,send_uid,send_uname):
	session = DBSession()
	try:
		session.add(Fengbao(realRoomid=realRoomid,send_uid=send_uid,send_uname=send_uname))
		queryUser=session.query(User).filter_by(realRoomid=realRoomid).first()
		if queryUser:
			queryUser.fengbaoNum+=1
		else:
			session.add(User(realRoomid=realRoomid,fengbaoNum=1))
		session.commit()
		session.close()
	except Exception as e:
		print(e)


# # 创建session对象:
# session = DBSession()
# # 创建新User对象
# new_user = User(uid=12,uname='喵咭喵呜',roomid=1273106,fansnum=12333,areaName='电子竞技')
# # 添加到session
# session.add(new_user)
# # 提交保存到数据库
# session.commit()
# # 关闭session
# session.close()

# 可见将关键是获取session, 然后把对象添加到session, 最后提交并关闭.(DBSession对象, 可以看做是当前数据库的连接)

# 查询
# session = DBSession()
# # 创建Query查询, filter是where条件, 最后调用one()返回唯一行, 如果调用all()则返回所有行.
# user = session.query(User).filter(User.uid==12722).one()
# print('type:', type(user))
# print('name:', user.uname)
# session.close()


####Relattionship SQLAlchemy中的映射关系有四种,分别是一对多,多对一,一对一,多对多
#####一对多(one to many） 因为外键(ForeignKey)始终定义在多的一方.如果relationship定义在多的一方,那就是多对一,一对多与多对一的区别在于其关联(relationship)的属性在多的一方还是一的一方，如果relationship定义在一的一方那就是一对多.
# 这里的例子中,一指的是Parent,一个parent有多个child.

# class Parent(Base):
#     __tablename__ = 'parent'
#     id = Column(Integer,primary_key = True)
#     children = relationship("Child",backref='parent')

# class Child(Base):
#     __tablename__ = 'child'
#     id = Column(Integer,primary_key = True)
#     parent_id = Column(Integer,ForeignKey('parent.id'))
