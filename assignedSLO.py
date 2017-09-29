from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'AssignedSLO'

    sloID = Column(String(3), primary_key=True)
    CRN = Column(String(5), primary_key=True)
    
    def __str__(self):
        return "User object: (id='%s')" % self.id
      
    def __init__(self,sloID, CRN):
      self.sloID = sloID
      self.CRN = CRN