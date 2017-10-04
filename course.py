from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Course(Base):
    __tablename__ = 'Course'
    
    CRN = Column(String(9), primary_key = True)
    course_name = Column(String(255))
    course_type = Column(String(25))
    faculty_id = Column(Integer(9))
    semester = Column(String(6))
    course_year = Column(Date)
    
    def __init__(self,CRN,course_name,course_type,faculty_id,semester,course_year):
      self.CRN = CRN
      self.course_name = course_name
      self.course_type = course_type
      self.faculty_id = faculty_id
      self.semester = semester
      self.course_year = course_year