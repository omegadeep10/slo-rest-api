from sqlalchemy import Column, Integer, String, Date, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.ext.hybrid import hybrid_property
import sys

Base = declarative_base()

registration = Table('Registration', Base.metadata,
    Column('crn', String(5), ForeignKey('Course.crn')),
    Column('student_id', String(9), ForeignKey('Student.student_id'))
)

# ASSOCIATIVE TABLES THAT NEED TO BE MAPPED LIKE ABOVE

class AssignedSLOModel(Base):
    __tablename__ = 'AssignedSLO'

    slo_id = Column(String(3), primary_key=True)
    crn = Column(String(5), primary_key=True)
    
    def __str__(self):
        return "AssignedSLO object: (slo_id='%s')" % self.slo_id
      
    def __init__(self,slo_id, crn):
      self.slo_id = slo_id
      self.crn = crn



# REGULAR TABLES

class CourseModel(Base):
    __tablename__ = 'Course'

    crn = Column(String(5), primary_key=True)
    faculty_id = Column(String(9), ForeignKey('Faculty.faculty_id'), nullable=False)
    course_name = Column(String(255), nullable=False)
    course_type = Column(String(25))
    semester = Column(String(6))
    course_year = Column(Date)
    faculty = relationship("FacultyModel", back_populates="courses")
    students = relationship("StudentModel", secondary=registration)

    def __str__(self):
      return "Course object: (crn='%s')" % self.crn
    
    def __init__(self, crn, faculty_id, course_name, course_type, semester, course_year):
      self.crn = crn
      self.faculty_id = faculty_id
      self.course_name = course_name
      self.course_type = course_type
      self.semester = semester
      self.course_year = course_year


class StudentModel(Base):
    __tablename__ = 'Student'
    
    student_id = Column(String(9), primary_key=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    
    def __str__(self):
      return "Student object: (student_id='%s')" % self.student_id

    def __init__(self, student_id, first_name, last_name):
      self.student_id = student_id
      self.first_name = first_name
      self.last_name = last_name




class FacultyModel(Base):
    __tablename__ = 'Faculty'
    
    id = Column(Integer, primary_key=True)
    email = Column(String(255))
    faculty_id = Column(String(9))
    first_name = Column(String(255))
    last_name = Column(String(255))
    _password = Column('password',String(255))
    user_type = Column(String(1))
    courses = relationship("CourseModel", back_populates="faculty")
    @hybrid_property
    def password(self):
      return self._password

    @password.setter
    def set_password(self, password):
      self._password = generate_password_hash(password)

    def check_password(self, password):
      print(password,file=sys.stderr)
      if check_password_hash(self._password, password):
        return True

      return False
    
    def __str__(self):
       return "Faculty object: (id='%s')" % self.id

    def __init__(self, email, faculty_id, first_name, last_name, password, user_type):
        self.email = email
        self.faculty_id = faculty_id
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.user_type = user_type




class AssessmentModel(Base):
    __tablename__ = 'assessment'

    assessment_id = Column(Integer, primary_key=True)
    crn = Column(String(5))
    slo_id = Column(String(3))
    student_id = Column(String(9))
    total_score = Column(Integer)
    
    def __str__(self):
        return "Assessment object: (assessment_id='%s')" % self.assessment_id
      
    def __init__(self, assessment_id, crn, slo_id, student_id, total_score):
      self.assessment_id = assessment_id
      self.crn = crn
      self.slo_id = slo_id
      self.student_id = student_id
      self.total_score = total_score



class SLOModel(Base):
  __tablename__ = 'SLO'

  slo_id = Column(String(9),primary_key = True)
  slo_description = Column(String(255))

  def __str__(self):
    return "SLO object: (slo_id='%s')" % self.slo_id

  def __init__(self,slo_id,slo_description):
    self.slo_id = slo_id
    self.slo_description = slo_description



class PerfIndicatorModel(Base):
    __tablename__ = 'PerformanceIndicator'
    
    performance_indicator_id = Column(String(5), primary_key=True)
    slo_id = Column(String(3))
    performance_indicator_description = Column(String(255))
    unsatisfactory_description = Column(String(255))
    developing_description = Column(String(255))
    satisfactory_description = Column(String(255))
    exempary_description = Column(String(255))

    def __str__(self):
      return "PerfIndicator object: (performance_indicator_id='%s')" % self.performance_indicator_id
    
    def __init__(self,performance_indicator_id,slo_id,performance_indicator_description,unsatisfactory_description,developing_description,satisfaction_description,exemplary_description):
      self.performance_indicator_id = performance_indicator_id
      self.slo_id = slo_id
      self.performance_indicator_description = performance_indicator_description
      self.unsatisfsctory_description = unsatisfactory_description
      self.developing_description = developing_description
      self.satisfactory_description = satisfaction_description
      self.exempary_description = exemplary_description



class ScoreModel(Base):
    __tablename__ = 'Score'
    
    performance_indicator_id = Column(String(255), primary_key=True)
    assessment_id = Column(Integer, primary_key=True)
    score = Column(Integer)

    def __str__(self):
      return "Score object: (performance_indicator_id='%s')" % self.performance_indicator_id
    
    def __init__(self,performance_indicator_id,assessment_id,score):
      self.performance_indicator_id = performance_indicator_id
      self.assessment_id = assessment_id
      self.score = score