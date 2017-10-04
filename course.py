from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Course(Base):
    __tablename__ = 'Course'
    
    crn = Column(String(9), primary_key = True)
    faculty_id = Column(String(9))
    course_name = Column(String(255))
    course_type = Column(String(25))
    semester = Column(String(6))
    course_year = Column(Date)
    
    def __init__(self,crn,faculty_id,course_name,course_type,semester,course_year):
      self.crn = crn
      self.faculty_id = faculty_id
      self.course_name = course_name
      self.course_type = course_type
      self.semester = semester
      self.course_year = course_year