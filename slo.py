from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class SLO(Base):
  __tablename__ = 'SLO'
  
  sloID = Column(String(9),primary_key = True)
  sloDesc = Column(String(255))
  
  def __init__(self,sloID,sloDesc):
    self.sloID = sloID
    self.sloDesc = sloDesc