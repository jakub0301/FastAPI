from sqlalchemy import Column, Integer, String
from post.database import Base

class Post(Base):
    __tablename__ = 'posts'
    
    id = Column(Integer, primary_key=True, index=True)
    body = Column(String)
    counter = Column(Integer)

class User(Base):
    __tablename__ = 'users'

    username = Column(String, primary_key=True)
    password = Column(Integer)
