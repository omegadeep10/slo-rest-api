from sqlalchemy import Column
from sqlalchemy import Char
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Student(Base):
    __tablename__ = 'Student'
    
    studID = Column(Char(9), primary_key=True)
    fname = Column(Char(25))
    lname = Column(Char(25))
    
    def __init__(self, studID, fname, lname):
      self.studID = studID
      self.fname = fname
      self.lname = lname