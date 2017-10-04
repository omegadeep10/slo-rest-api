from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Faculty(Base):
    __tablename__ = 'Faculty'
    
    id = Column(Integer, primary_key=True)
    email = Column(String(255))
    faculty_id = Column(String(9))
    first_name = Column(String(255))
    last_name = Column(String(255))
    password = Column(String(255))
    userType = Column(String(1))
    
    def __str__(self):
       return "User object: (id='%s')" % self.id

    def __init__(self,email,faculty_id,first_name,last_name,password,userType):
        self.email = email
        self.faculty_id = faculty_id
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.userType = userType 