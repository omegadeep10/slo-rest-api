from sqlalchemy import Column, Integer, String, Date, ForeignKey, Table, Boolean
from sqlalchemy import select, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship, backref, column_property
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.ext.hybrid import hybrid_property
import sys
from db import session

Base = declarative_base()

registration = Table('Registration', Base.metadata,
    Column('crn', String(5), ForeignKey('Course.crn')),
    Column('student_id', String(9), ForeignKey('Student.student_id'))
)

# REGULAR TABLES

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
    scores = relationship("ScoreModel")
    
    def __str__(self):
        return "Assessment object: (course='%s')" % self.course.crn
      
    def __init__(self, crn, slo_id, student_id, total_score):
      self.crn = crn
      self.slo_id = slo_id
      self.student_id = student_id
      self.total_score = total_score



class CourseModel(Base):
    __tablename__ = 'Course'

    crn = Column(String(5), primary_key=True)
    faculty_id = Column(String(9), ForeignKey('Faculty.faculty_id'), nullable=False)
    course_number = Column(String(5), nullable=False)
    course_name = Column(String(255), nullable=False)
    course_type = Column(String(25))
    semester = Column(String(6))
    course_year = Column(Date)
    
    faculty = relationship("FacultyModel", back_populates="courses")
    students = relationship("StudentModel", secondary=registration,back_populates="courses")
    assessments_count = column_property(select([func.count(AssessmentModel.assessment_id)]).where(AssessmentModel.crn == crn))
    assigned_slos = association_proxy("assigned_slos", "slo") # List of AssignedSLO objects

    @property
    def completion(self):
      students_count = len(self.students)
      slos_count = len(self.assigned_slos)
      total = students_count * slos_count
      if (total and total == self.assessments_count):
        return True
      else:
        return False

    def __str__(self):
      return "Course object: (crn='%s')" % self.crn
    
    def __init__(self, crn, faculty_id, course_number, course_name, course_type, semester, course_year):
      self.crn = crn
      self.faculty_id = faculty_id
      self.course_number = course_number
      self.course_name = course_name
      self.course_type = course_type
      self.semester = semester
      self.course_year = course_year



class AssignedSLOModel(Base):
  __tablename__ = "AssignedSLO"

  crn = Column(String(5), ForeignKey('Course.crn'), primary_key=True)
  slo_id = Column(String(3), ForeignKey('SLO.slo_id'), primary_key=True)
  comments = Column(String)

  course = relationship(CourseModel, backref=backref("assigned_slos", cascade="all, delete-orphan"))
  slo = relationship("SLOModel", backref=backref("courses", cascade="all, delete-orphan"))

  def __str__(self):
    return "test"

  def __init__(self, crn, slo_id, comments):
    self.slo_id = slo_id
    self.crn = crn
    self.comments = comments


class SLOModel(Base):
  __tablename__ = 'SLO'

  slo_id = Column(String(9),primary_key = True)
  slo_description = Column(String(255))
  archived = Column(Boolean, unique=False, default=False)
  performance_indicators = relationship("PerfIndicatorModel", back_populates="slos")
  courses = association_proxy("courses", "course")

  def __str__(self):
    return "SLO object: (slo_id='%s')" % self.slo_id

  def __init__(self,slo_id,slo_description):
    self.slo_id = slo_id
    self.slo_description = slo_description



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
    
    def __init__(self, performance_indicator_id, slo_id, performance_indicator_description, unsatisfactory_description, developing_description, satisfactory_description, exemplary_description):
      self.performance_indicator_id = performance_indicator_id
      self.slo_id = slo_id
      self.performance_indicator_description = performance_indicator_description
      self.unsatisfactory_description = unsatisfactory_description
      self.developing_description = developing_description
      self.satisfactory_description = satisfactory_description
      self.exemplary_description = exemplary_description



class ScoreModel(Base):
    __tablename__ = 'Score'
    
    performance_indicator_id = Column(String(5), ForeignKey('PerformanceIndicator.performance_indicator_id'), primary_key=True)
    assessment_id = Column(Integer, ForeignKey('Assessment.assessment_id'), primary_key=True)
    score = Column(Integer)
    performance_indicators = relationship("PerfIndicatorModel",back_populates="scores")

    def __str__(self):
      return "Score object: (performance_indicator_id='%s')" % self.performance_indicator_id
    
    def __init__(self,performance_indicator_id,assessment_id,score):
      self.performance_indicator_id = performance_indicator_id
      self.assessment_id = assessment_id
      self.score = score