from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class PerfIndicator(Base):
    __tablename__ = 'PerfIndicator'
    
    perfID = Column(String(5),primary_key=True)
    sloID = Column(String(3))
    perfDesc = Column(String(255))
    unsatDesc = Column(String(255))
    develDesc = Column(String(255))
    satisDesc = Column(String(255))
    exempDesc = Column(String(255))
    
    def __init__(self,perfID,sloID,perfDesc,unsatDesc,develDesc,satisDesc,exempDesc):
      self.perfID = perfID
      self.sloID = sloID
      self.perfDesc = perfDesc
      self.unsatDesc = unsatDesc
      self.develDesc = develDesc
      self.satisDesc = satisDesc
      self.exempDesc = exempDesc
    