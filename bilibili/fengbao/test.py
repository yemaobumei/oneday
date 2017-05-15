# # 在Python中, 最有名的ORM框架是SQLAlchemy. 我们来看看SQLAlchemy的用法.

# from sqlalchemy import Column, String,Integer, create_engine,engine
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base

from sql import *
# 初始化数据库连接
engine = create_engine('sqlite:///ye.db', echo=True)
# 创建DBSession类型
DBSession = sessionmaker(bind=engine)

# 查询
session = DBSession()
# 创建Query查询, filter是where条件, 最后调用one()返回唯一行, 如果调用all()则返回所有行.
user = session.query(User).filter(User.uid==12).one()
print('type:', type(user))
print('name:', user.uname)
session.close()