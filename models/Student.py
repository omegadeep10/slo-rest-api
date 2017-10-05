from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Student(Base):
    __tablename__ = 'Student'
    
    student_id = Column(String(255), primary_key=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    
    def __init__(self, student_id, first_name, last_name):
      self.student_id = student_id
      self.first_name = first_name
      self.last_name = last_name