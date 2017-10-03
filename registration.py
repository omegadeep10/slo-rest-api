from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Registration(Base):
    __tablename__ = 'Registration'
    
    CRN = Column(String(9),primary_key=True)
    studID = Column(String(9),primary_key=True)
    
    def __init__(self,CRN,studID):
      self.CRN = CRN
      self.studID = studID
