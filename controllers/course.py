from flask_jwt import jwt_required, current_identity
from flask_restful import Resource, reqparse, marshal_with, fields
from controllers.auth import checkadmin
from db import session
from models.Course import Course
from datetime import datetime

class_fields = {
  'crn': fields.String,
  'faculty_id': fields.String,
  'course_name': fields.String,
  'course_type': fields.String,
  'semester': fields.String,
  'course_year': fields.String(attribute=lambda x: x.course_year.year) # extract only the Year as a string
}

classParser = reqparse.RequestParser()
classParser.add_argument('crn', type=str, required=True, help='CRN is required.')
classParser.add_argument('faculty_id', type=str, required=True, help='Faculty ID is required.')
classParser.add_argument('course_name', type=str, required=True,help='Course name is required.')
classParser.add_argument('course_type', type=str, required=True, help='Course type is required.')
classParser.add_argument('semester', type=str, required=True, help='Semester is required.')
classParser.add_argument('course_year', type=datetime.fromtimestamp, required=True, help='Course year is required.')

class Course(Resource):
  @jwt_required()
  @marshal_with(class_fields)
  def get(self, crn):
    return session.query(Course).filter(Course.crn == crn).first()
  
  def put(self, crn):
    classParserCopy = classParser.copy()
    classParserCopy.remove_argument('crn')
    args = classParserCopy.parse_args()

    course = session.query(Course).filter(Course.crn == crn).first()
    course.faculty_id = args['faculty_id']
    course.course_name = args['course_name']
    course.course_type = args['course_type']
    course.course_year = args['course_year']
    course.semester = args['semester']

    session.commit()
    
  
  def delete(self, crn):
    return {'data4':'deleted successfully'}
  
class CourseList(Resource):
  @jwt_required()
  @marshal_with(class_fields)
  def get(self):
    return session.query(Course).filter(Course.faculty_id == current_identity.faculty_id).all()
  
  @marshal_with(class_fields)
  def post(self):
    args = classParser.parse_args()
    me = Course(args['crn'], args['faculty_id'], args['course_name'], args['course_type'], args['semester'], args['course_year'])
    session.add(me)
    session.commit() #commits to a database
    return me