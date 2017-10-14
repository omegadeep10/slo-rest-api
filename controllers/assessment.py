from flask_jwt import jwt_required, current_identity
from flask_restful import Resource, reqparse, marshal_with, fields, abort
from controllers.auth import checkadmin
from db import session
from models import AssessmentModel
from marshal_base_fields import student_fields, class_fields, slo_fields, score_fields

parser = reqparse.RequestParser()
parser.add_argument('crn', type=str, required = True, help='Student ID field is required.')
parser.add_argument('slo_id', type=str, required = True, help='SLO ID field is required.')
parser.add_argument('student_id', type=str, required = True, help='Total Score is required.')
parser.add_argument('performance_indicator_id', type=str, required= True, help='Performance Indicator ID is required')
parser.add_argument('score', type=int, required= True, help='Score is required')


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
  method_decorators= [jwt_required()]

  @marshal_with(assessment_fields)
  def get(self,assessment_id):
    return session.query(AssessmentModel).filter(AssessmentModel.assessment_id == assessment_id).first()
  
  def put(self):
    return { 'data3': 'assessment updated' }
  
  def delete(self):
    return { 'data4': 'deleted successfully' }


class AssessmentList(Resource):
  method_decorators = [jwt_required()]

  @marshal_with(assessment_fields)
  def get(self, crn):
    return session.query(AssessmentModel).filter(AssessmentModel.crn == crn).all()
