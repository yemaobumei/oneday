# 在Python中, 最有名的ORM框架是SQLAlchemy. 我们来看看SQLAlchemy的用法.

from sqlalchemy import Column, String,Integer, DateTime, create_engine,engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.sql import func

Base = declarative_base()
class User(Base):
    # 表的名字
    __tablename__ = 'user'

    # 表的结构
    uid = Column(Integer,  primary_key=True)
    uname = Column(String(20),nullable=False)
    roomid = Column(Integer,nullable=True)
    real_roomid = Column(Integer,nullable=True)
    fansnum = Column(Integer,nullable=True)
    areaName = Column(String(20),nullable=True)
    date = Column(DateTime(timezone=True), default=func.now())

class SmallTv(Base):
	__tablename__ = 'TvRecord'
	tv_id = Column(Integer, primary_key=True)
	roomid = Column(Integer,nullable=False)
	real_roomid = Column(Integer,nullable=True)
	#date = Column(Date, default=datetime.today().strftime("%Y-%m-%d"), nullable=False)
	date = Column(DateTime(timezone=True), default=func.now())

class Fengbao(Base):
	__tablename__ = 'Fengbao'
	id = Column(Integer,primary_key=True)
	roomid = Column(Integer)
	date = Column(DateTime(timezone=True), default=func.now())


# # 初始化数据库连接
# engine = create_engine('sqlite:///ye.db', echo=True)
# # 创建DBSession类型
# DBSession = sessionmaker(bind=engine)

# # # 建立表
# Base.metadata.create_all(engine)#新建数据库文件，必须使用此语句建立表结构，以后打开可以不加此语句。

# create_engine用来初始化数据库连接.
# SQLAlchemy用一个字符串表示连接信息'数据库类型+数据库驱动名称://用户名:口令@机器地址:端口号/数据库名'

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

# # 查询
# session = DBSession()
# # 创建Query查询, filter是where条件, 最后调用one()返回唯一行, 如果调用all()则返回所有行.
# user = session.query(User).filter(User.uid==12).one()
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
