from flask_jwt import jwt_required, current_identity
from flask_restful import Resource, fields, marshal_with, abort, reqparse
from controllers.auth import checkadmin
from db import session
from models.Course import CourseModel
from datetime import datetime

course_fields = {
  'crn': fields.String,
  'faculty_id': fields.String,
  'course_name': fields.String,
  'course_type': fields.String,
  'semester': fields.String,
  'course_year': fields.String(attribute=lambda x: x.course_year.year) # extract only the Year as a string
}


courseParser = reqparse.RequestParser()
courseParser.add_argument('crn', type=str, required=True)
courseParser.add_argument('faculty_id', type=str, required=True)
courseParser.add_argument('course_name', type=str, required=True)
courseParser.add_argument('course_type', type=str, required=True)
courseParser.add_argument('semester', type=str, required=True)
courseParser.add_argument('course_year', type=datetime.fromtimestamp, required=True)

class Course(Resource):
  @jwt_required()
  @marshal_with(course_fields)
  def get(self, crn):
    return session.query(CourseModel).filter(CourseModel.crn == crn).first()
  
  def put(self, crn):
    return {'data':'edited successfully'}
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
  
  @jwt_required()
  @marshal_with(course_fields)
  def post(self):
    parsed_args = courseParser.parse_args()
    x = CourseModel(
      crn=parsed_args['crn'],
      faculty_id=parsed_args['faculty_id'],
      course_name=parsed_args['course_name'],
      course_type=parsed_args['course_type'],
      semester=parsed_args['semester'],
      course_year=parsed_args['course_year']
    )

    session.add(x)
    session.commit()

    return x, 201