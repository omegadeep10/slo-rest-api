from flask_jwt import jwt_required, current_identity
from flask_restful import Resource, reqparse, marshal_with, fields, abort
from controllers.auth import checkadmin
from db import session
from models import CourseModel, SLOModel, AssignedSLOModel
from datetime import datetime
from marshal_base_fields import class_fields, faculty_fields, assigned_slo_fields, student_fields
import sys

class_extra_fields = {
  'faculty': fields.Nested(faculty_fields),
  'assigned_slos': fields.Nested(assigned_slo_fields),
  'completion': fields.Boolean 
}

class_student_fields = {
  'students': fields.List(fields.Nested(student_fields)),
}

def slosList(slo):
  if 'slo_id' not in slo or 'comments' not in slo:
    raise ValueError("All slos must contain a slo_id and comments field. The comments field may be null.")

  if type(slo['slo_id']) is not str:
    raise ValueError("SLO must be a string.") 

  return slo

# Default class parser.
classParser = reqparse.RequestParser()
classParser.add_argument('crn', type=str, required=True, help='CRN is required.')
classParser.add_argument('faculty_id', type=str, required=True, help='Faculty ID is required.')
classParser.add_argument('course_name', type=str, required=True,help='Course name is required.')
classParser.add_argument('course_type', type=str, required=True, help='Course type is required.')
classParser.add_argument('semester', type=str, required=True, help='Semester is required.')
classParser.add_argument('course_year', type=datetime.fromtimestamp, required=True, help='Course year is required.')
classParser.add_argument('slos', type=slosList, required=True, help="Assigned SLOs are required.", action='append')

class Course(Resource):
  method_decorators = [jwt_required()]
  
  @marshal_with({**class_fields, **class_extra_fields, **class_student_fields})
  def get(self, crn):
    return session.query(CourseModel).filter(CourseModel.crn == crn).first()
  
  
  @marshal_with({**class_fields, **class_extra_fields, **class_student_fields})
  def put(self, crn):
    classParserCopy = classParser.copy() # Initialize a copy of standard classParser and remove crn argument
    classParserCopy.remove_argument('crn')
    args = classParserCopy.parse_args()

    # Get the course object from db
    course = session.query(CourseModel).filter(CourseModel.crn == crn).first()
    # If course doesn't exist, abort
    if not course: 
      return abort(404, message="Course with the crn {} doesn't exist".format(crn))

    validSLOs = [] # If SLO exists, create an AssignedSLOModel object and add to this list
    
    for sloObject in args['slos']: # For each SLO passed in
      slo = session.query(SLOModel).filter(SLOModel.slo_id == sloObject['slo_id']).one_or_none() # Get the SLO object
      
      if slo:
        validSLOs.append(AssignedSLOModel(crn, sloObject['slo_id'], sloObject['comments']))
      else: # If SLO doesn't exist, abort
        abort(404, message="SLO with this slo_id {} does not exist.".format(slo['slo_id']))


<<<<<<< HEAD
    else:
      return abort(404, message="Course with the crn {} doesn't exist".format(crn))

=======
    # at this point, all data is valid, so commence updating the course object
    course.assigned_slos = validSLOs # Replace assigned_slos with new list of AssignedSLOModels. SQLAlchemy will figure it out
    course.faculty_id = args['faculty_id']
    course.course_name = args['course_name']
    course.course_type = args['course_type']
    course.course_year = args['course_year']
    course.semester = args['semester']

    session.commit()
    return course
>>>>>>> master
  

  def delete(self, crn):
    course = session.query(CourseModel).filter(CourseModel.crn == crn).first()
    if (course):
      session.delete(course)
      session.commit()
      return {}, 204 # Delete successful, so return empty 204 successful response
      
    else:
      abort(404, message="Course with the crn {} doesn't exist".format(crn)) # If class with the specified CRN doens't exist, return 404

  

class CourseList(Resource):
  method_decorators = [jwt_required()]
  
  @marshal_with({**class_fields, **class_extra_fields})
  def get(self):
    return session.query(CourseModel).filter(CourseModel.faculty_id == current_identity.faculty_id).all()

  
  
  @marshal_with({**class_fields, **class_extra_fields})
  def post(self):
    args = classParser.parse_args() 
    newCourse = CourseModel(args['crn'], args['faculty_id'], args['course_name'], args['course_type'], args['semester'], args['course_year'])
    
    validSLOs= []
    for sloObject in args['slos']:
      slo = session.query(SLOModel).filter(SLOModel.slo_id == sloObject['slo_id']).one_or_none()
      
      if slo:
        validSLOs.append(AssignedSLOModel(args['crn'], sloObject['slo_id'], sloObject['comments']))
      else:
        abort(404, message="SLO with this slo_id {} does not exist.".format(slo['slo_id']))
    
    session.add(newCourse)
    newCourse.assigned_slos = validSLOs
    
    session.commit() #commits to a database
    return newCourse