from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'Logins'

    id = Column(Integer, primary_key=True)
    email = Column(String(45))
    fname = Column(String(20))
    lname = Column(String(20))
    password = Column(String(45))
    userType = Column(String(1))
    
    def __str__(self):
        return "User object: (id='%s')" % self.id
      
    def __init__(self,email,fname,lname,password,userType):
      self.email = email
      self.fname = fname
      self.lname = lname
      self.password = password
      self.userType = userType