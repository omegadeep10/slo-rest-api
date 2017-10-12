from flask_jwt import jwt_required, current_identity
from flask_restful import Resource
from controllers.auth import checkadmin
from db import session
from models import AssessmentModel

class Assessment(Resource):
  @jwt_required()
  def get(self,assessment_id):
    return session.query(AssessmentModel).filter(AssessmentModel.assessment_id == assessment_id)
  
  def post(self):
    return {'data':'post assessment object'}
  
  def put(self):
    return {'data3':'assessment updated'}
  
  def delete(self):
    return {'data4':'deleted successfully'}
  
class AssessmentList(Resource):
  @jwt_required()
  def get(self):
    return session.query(AssessmentModel).filter(AssessmentModel)