# 在Python中, 最有名的ORM框架是SQLAlchemy. 我们来看看SQLAlchemy的用法.

from sqlalchemy import Column, String,Integer, create_engine,engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
class User(Base):
    # 表的名字
    __tablename__ = 'user'

    # 表的结构
    uid = Column(Integer,  primary_key=True)
    uname = Column(String(20))
    roomid = Column(Integer)
    fansnum = Column(Integer)
    areaName = Column(String(20))





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

# ORM就是把数据库表的行与相应的对象简历关联, 互相转换.
# 由于关系数据库的多个表还可以用外键实现一对多, 多对多的关联, 相应地, ORM框架也可以提供两个对象之间的一对多, 多对多功能.
# 例如, 如果一个User拥有多个Book, 就可以定义一对多关系如下
# class User(Base):
#     __tablename__ = 'user'
#
#     id = Column(String(20), primary_key=True)
#     name = Column(String(20))
#     books = relationship('BOOK')
#
# class BOOK(Base):
#     __tablename__ = 'book'
#     id = Column(String(20), primary_key=True)
#     nam = Column(String(20))
#     user_id = Column(String(20), ForeignKey('user.id'))
