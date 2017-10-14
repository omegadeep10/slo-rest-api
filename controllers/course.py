from flask_jwt import jwt_required, current_identity
from flask_restful import Resource, reqparse, marshal_with, fields, abort
from controllers.auth import checkadmin
from db import session
from models import CourseModel
from datetime import datetime
from marshal_base_fields import class_fields, faculty_fields, slo_fields, student_fields

class_extra_fields = {
  'faculty': fields.Nested(faculty_fields),
  'slos': fields.Nested(slo_fields)
}


class_student_fields = {
  'students': fields.List(fields.Nested(student_fields)),
}

# Default class parser.
classParser = reqparse.RequestParser()
classParser.add_argument('crn', type=str, required=True, help='CRN is required.')
classParser.add_argument('faculty_id', type=str, required=True, help='Faculty ID is required.')
classParser.add_argument('course_name', type=str, required=True,help='Course name is required.')
classParser.add_argument('course_type', type=str, required=True, help='Course type is required.')
classParser.add_argument('semester', type=str, required=True, help='Semester is required.')
classParser.add_argument('course_year', type=datetime.fromtimestamp, required=True, help='Course year is required.')
classParser.add_argument('comments',type=str)

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

    course = session.query(CourseModel).filter(CourseModel.crn == crn).first()
    if (course):
      course.faculty_id = args['faculty_id']
      course.course_name = args['course_name']
      course.course_type = args['course_type']
      course.course_year = args['course_year']
      course.semester = args['semester']

      session.commit()
      return course

    else:
      return abort(404, message="Course with the crn {} doesn't exist".format(crn))
  

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
    newCourse = CourseModel(args['crn'], args['faculty_id'], args['course_name'], args['course_type'], args['semester'], args['course_year'],args['comments'])
    session.add(newCourse)
    session.commit() #commits to a database
    return newCourse