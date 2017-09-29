from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects import Year

Base = declarative_base()

class Course(Base):
    __tablename__ = 'Course'
    
    CRN = Column(String(9), primary_key = True)
    courseName = Column(String(150))
    courseType = Column(String(25))
    id = Column(Integer)
    semester = Column(String(6))
    courseYear = Column(Year)
    
    def __init__(self,CRN,courseName,courseType,id,semester,courseYear):
      self.CRN = CRN
      self.courseName = courseName
      self.courseType = courseType
      self.id = id
      self.semester = semester
      self.courseYear = courseYear