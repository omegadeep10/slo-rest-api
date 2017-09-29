from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'assessment'

    assessID = Column(Integer(7), primary_key=True)
    CRN = Column(String(5))
    sloID = Column(String(3))
    studID = Column(String(9))
    totalVal = Column(Integer(5))
    
    def __str__(self):
        return "User object: (id='%s')" % self.id
      
    def __init__(self,assessID,CRN,sloID,studID,totalVal):
      self.assessID = assessID
      self.CRN = CRN
      self.sloID = sloID
      self.studID = studID
      self.totalVal = totalVal