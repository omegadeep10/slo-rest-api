from flask_jwt import jwt_required, current_identity
from flask_restful import Resource, reqparse, marshal_with, fields
from controllers.auth import checkadmin
from db import session
from course import Course 
import sys
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

class Classes(Resource):
  @jwt_required()
  def get(self,crn):
    return {'data':'CRN'}
  
  def get_crn(self):
    return {'data1':'get crn'}
  
  def put(self):
    return {'data3':'edited successfully'}
  
  def delete(self):
    return {'data4':'deleted successfully'}
  
class ClassesList(Resource):
  @jwt_required()
  @marshal_with(class_fields)
  def get(self):
    classParser.add_argument('faculty_id', type=str, required=True, help='Faculty ID is required.')
    args = classParser.parse_args()
    user_id = args['faculty_id']
    return session.query(Course).filter(Course.faculty_id == user_id).all()

  def post(self):
    classParser.add_argument('crn', type=str, required=True, help='CRN is required.')
    classParser.add_argument('faculty_id', type=str, required=True, help='Faculty ID is required.')
    classParser.add_argument('course_name', type=str, required=True,help='Course name is required.')
    classParser.add_argument('course_type', type=str, required=True, help='Course type is required.')
    classParser.add_argument('semester', type=str, required=True, help='Semester is required.')
    classParser.add_argument('course_year', type=datetime.fromtimestamp, required=True, help='Course year is required.')
    args = classParser.parse_args()
    me = Course(args['crn'],args['faculty_id'],args['course_name'],args['course_type'],args['semester'],args['course_year'])
    session.add(me)
    session.commit() #commits to a database
    return me