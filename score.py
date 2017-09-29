from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Char
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Score(Base):
    __tablename__ = 'Score'
    
    perfID = Column(Char(5) primary_key=True),
    assessID = Column(Integer(7) primary_key=True),
    scoreVal = Column(Integer(2))
    
    def __init__(self,perfID,assessID,scoreVal):
      self.perfID = perfID
      self.assessID = assessID
      self.scoreVal = scoreVal