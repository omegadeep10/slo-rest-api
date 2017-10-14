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

assignedslo = Table('AssignedSLO',Base.metadata,
    Column('crn', String(5), ForeignKey('Course.crn')),
    Column('slo_id', String(3), ForeignKey('SLO.slo_id'))
)

# REGULAR TABLES

class CourseModel(Base):
    __tablename__ = 'Course'

    crn = Column(String(5), primary_key=True)
    faculty_id = Column(String(9), ForeignKey('Faculty.faculty_id'), nullable=False)
    course_name = Column(String(255), nullable=False)
    course_type = Column(String(25))
    semester = Column(String(6))
    course_year = Column(Date)
    comments = Column(String(2500))
    faculty = relationship("FacultyModel", back_populates="courses")
    students = relationship("StudentModel", secondary=registration,back_populates="courses")
    slos = relationship("SLOModel",secondary=assignedslo)

    def __str__(self):
      return "Course object: (crn='%s')" % self.crn
    
    def __init__(self, crn, faculty_id, course_name, course_type, semester, course_year, comments):
      self.crn = crn
      self.faculty_id = faculty_id
      self.course_name = course_name
      self.course_type = course_type
      self.semester = semester
      self.course_year = course_year
      self.comments = comments


class StudentModel(Base):
    __tablename__ = 'Student'
    
    student_id = Column(String(9), primary_key=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    courses = relationship("CourseModel",secondary=registration,back_populates="students")
    
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
    __tablename__ = 'Assessment'

    assessment_id = Column(Integer, primary_key=True)
    crn = Column(String(5), ForeignKey('Course.crn'))
    slo_id = Column(String(3), ForeignKey('SLO.slo_id'))
    student_id = Column(String(9), ForeignKey('Student.student_id'))
    total_score = Column(Integer)
    course = relationship("CourseModel")
    student = relationship("StudentModel")
    slo = relationship("SLOModel")
    scores = relationship("ScoreModel",back_populates="assessments")
    
    def __str__(self):
        return "Assessment object: (course='%s')" % self.course.crn
      
    def __init__(self, crn, slo_id, student_id, total_score):
      self.crn = crn
      self.slo_id = slo_id
      self.student_id = student_id
      self.total_score = total_score



class SLOModel(Base):
  __tablename__ = 'SLO'

  slo_id = Column(String(9),primary_key = True)
  slo_description = Column(String(255))
  performance_indicators = relationship("PerfIndicatorModel", back_populates="slos")
  courses = relationship("CourseModel",secondary=assignedslo, back_populates="slos")

  def __str__(self):
    return "SLO object: (slo_id='%s')" % self.slo_id

  def __init__(self,slo_id,slo_description):
    self.slo_id = slo_id
    self.slo_description = slo_description



class PerfIndicatorModel(Base):
    __tablename__ = 'PerformanceIndicator'
    
    performance_indicator_id = Column(String(5), primary_key=True)
    slo_id = Column(String(3), ForeignKey('SLO.slo_id'))
    performance_indicator_description = Column(String(255))
    unsatisfactory_description = Column(String(255))
    developing_description = Column(String(255))
    satisfactory_description = Column(String(255))
    exemplary_description = Column(String(255))
    slos = relationship("SLOModel", back_populates="performance_indicators")
    scores = relationship("ScoreModel",back_populates="performance_indicators")

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
    
    performance_indicator_id = Column(String(5), ForeignKey('PerformanceIndicator.performance_indicator_id'), primary_key=True)
    assessment_id = Column(Integer, ForeignKey('Assessment.assessment_id'), primary_key=True)
    score = Column(Integer)
    assessments = relationship("AssessmentModel",back_populates="scores")
    performance_indicators = relationship("PerfIndicatorModel",back_populates="scores")

    def __str__(self):
      return "Score object: (performance_indicator_id='%s')" % self.performance_indicator_id
    
    def __init__(self,performance_indicator_id,assessment_id,score):
      self.performance_indicator_id = performance_indicator_id
      self.assessment_id = assessment_id
      self.score = score