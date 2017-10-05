from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Assessment(Base):
    __tablename__ = 'assessment'

    assessment_id = Column(Integer(11), primary_key=True)
    CRN = Column(String(5))
    slo_id = Column(String(3))
    student_id = Column(String(9))
    total_score = Column(Integer(11))
    
    def __str__(self):
        return "User object: (id='%s')" % self.id
      
    def __init__(self,assessment_id,CRN,slo_id,student_id,total_score):
      self.assessment_id = assessment_id
      self.CRN = CRN
      self.slo_id = slo_id
      self.student_id = student_id
      self.total_score = total_score