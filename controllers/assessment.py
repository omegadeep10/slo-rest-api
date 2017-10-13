from flask_jwt import jwt_required, current_identity
from flask_restful import Resource, reqparse, marshal_with, fields, abort
from controllers.auth import checkadmin
from db import session
from models import AssessmentModel
import sys, pickle

parser = reqparse.RequestParser()
parser.add_argument('student_id', type=str, required = True, help='Email field is required.')
parser.add_argument('slo_id', type=str, required = True, help='Student First Name field is required.')
parser.add_argument('last_name', type=str, required = True, help='L is required.')
parser.add_argument('crn', type=str, required = True, help='CRN field is required.')

faculty_fields = {
	'faculty_id': fields.String,
	'first_name': fields.String,
	'last_name': fields.String
}

class_fields = {
  'crn': fields.String,
  'course_name': fields.String,
  'course_type': fields.String,
  'semester': fields.String,
  'course_year': fields.String(attribute=lambda x: x.course_year.year), # extract only the Year as a string
  # 'comments': fields.String, # Don't need comments
  # 'faculty': fields.Nested(faculty_fields) # Don't need faculty
}

student_fields = {
	'student_id': fields.String,
	'first_name': fields.String,
	'last_name': fields.String
}

slo_fields = {
	'slo_id': fields.String,
	'slo_description': fields.String
}

score_fields = {
  'performance_indicator_id': fields.String,
  'score': fields.Integer
}

assessment_fields = {
  'assessment_id': fields.Integer,
  'slo_id': fields.String,
  'total_score': fields.Integer,
  'student': fields.Nested(student_fields),
  'course': fields.Nested(class_fields),
  'slo': fields.Nested(slo_fields),
  'scores': fields.List(fields.Nested(score_fields))
}

class Assessment(Resource):
  @jwt_required()
  @marshal_with(assessment_fields)
  def get(self,assessment_id):
    return session.query(AssessmentModel).filter(AssessmentModel.assessment_id == assessment_id).first()
  
  def put(self):
    return {'data3':'assessment updated'}
  
  def delete(self):
    return {'data4':'deleted successfully'}
  
class AssessmentList(Resource):
  @jwt_required()
  def get(self):
    return session.query(AssessmentModel).filter(AssessmentModel)