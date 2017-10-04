from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Char
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Score(Base):
    __tablename__ = 'Score'
    
    performance_indicator_id = Column(String(500) primary_key=True),
    assessment_id = Column(Integer(11) primary_key=True),
    score = Column(Integer(11))
    
    def __init__(self,performance_indicator_id,assessment_id,score):
      self.performance_indicator_id = performance_indicator_id
      self.assessment_id = assessment_id
      self.score = score
