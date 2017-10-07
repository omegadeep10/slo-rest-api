from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Registration(Base):
    __tablename__ = 'Registration'
    
    CRN = Column(String(9),primary_key=True)
    student_id = Column(String(9),primary_key=True)

    def __str__(self):
      return "Registration object: (crn='%s')" % self.crn
    
    def __init__(self,CRN,student_id):
      self.CRN = CRN
      self.student_id = student_id
