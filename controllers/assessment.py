from flask_jwt import jwt_required, current_identity
from flask_restful import Resource, reqparse
from controllers.auth import checkadmin
from db import session
from models import AssessmentModel

parser = reqparse.RequestParser()
parser.add_argument('student_id', type=str, required = True, help='Email field is required.')
parser.add_argument('slo_id', type=str, required = True, help='Student First Name field is required.')
parser.add_argument('last_name', type=str, required = True, help='L is required.')
parser.add_argument('crn', type=str, required = True, help='CRN field is required.')

class Assessment(Resource):
  @jwt_required()
  def get(self,assessment_id):
    return session.query(AssessmentModel).filter(AssessmentModel.assessment_id == assessment_id)
  
  def put(self):
    return {'data3':'assessment updated'}
  
  def delete(self):
    return {'data4':'deleted successfully'}
  
class AssessmentList(Resource):
  @jwt_required()
  def get(self):
    return session.query(AssessmentModel).filter(AssessmentModel)