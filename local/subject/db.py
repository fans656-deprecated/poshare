# coding: utf-8
import os
import urlparse

from flask import g

import psycopg2 as db
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 创建数据库连接
url = os.environ.get('DATABASE_URL') or 'sqlite:///data.db'
engine = create_engine(url)
session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
Base.query = session.query_property()

# 课程
class Subject(Base):

    __tablename__ = 'subjects'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)

def init_db():
    Base.metadata.drop_all(bind=engine) # 删除所有表
    Base.metadata.create_all(bind=engine) # 创建新的表
    # 从html文件中读取课程信息
    names = [t[:-5] for t in os.listdir(u'./descriptions') if t.endswith('html')]
    subjects = [
            Subject(name=name,
                description=open(u'./descriptions/{}.html'.format(name)).read().decode('utf-8'))
            for name in names]
    # 添加表的内容
    session.add_all(subjects)
    session.commit()
