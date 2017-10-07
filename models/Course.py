from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class CourseModel(Base):
    __tablename__ = 'Course'

    crn = Column(String(5), primary_key=True)
    faculty_id = Column(String(9), unique=True, nullable=False)
    course_name = Column(String(255), nullable=False)
    course_type = Column(String(25))
    semester = Column(String(6))
    course_year = Column(Date)
    
    def __str__(self):
        return "Course object: (crn='%s')" % self.crn
      
    def __init__(self, crn, faculty_id, course_name, course_type, semester, course_year):
        self.crn = crn
        self.faculty_id = faculty_id
        self.course_name = course_name
        self.course_type = course_type
        self.semester = semester
        self.course_year = course_year
