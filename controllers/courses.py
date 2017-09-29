from flask_jwt import jwt_required, current_identity
from flask_restful import Resource, fields, marshal_with, abort, reqparse
from controllers.auth import checkadmin
from db import session
from models.Course import CourseModel

course_fields = {
  'crn': fields.String,
  'faculty_id': fields.String,
  'course_name': fields.String,
  'course_type': fields.String,
  'semester': fields.String,
  'course_year': fields.String(attribute=lambda x: x.course_year.year) # extract only the Year as a string
}


class Course(Resource):
  @jwt_required()
  def get(self, crn):
    return {'data':'get classes'}
    # To-Do => Return specific course by CRN
  
  def put(self, crn):
    return {'data3':'edited successfully'}
    # To-Do => Edit a course
  
  def delete(self, crn):
    return {'data4':'deleted successfully'}
    # To-Do => Delete a specific course


class CourseList(Resource):
  @jwt_required()
  @marshal_with(course_fields)
  def get(self):
    if current_identity.user_type == '1':
      return session.query(CourseModel).all()
    else:
      return session.query(CourseModel).filter(CourseModel.faculty_id == current_identity.faculty_id).all()
  
  def post(self):
    return {'data2':'new crn'}
    # To-Do => Insert a new course