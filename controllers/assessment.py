from flask_jwt import jwt_required, current_identity
from flask_restful import Resource
from controllers.auth import checkadmin
from db import session
from models.Faculty import Faculty

class Assessment(Resource):
  @jwt_required()
  def get(self,assessment_id):
    return {'data1': 'assessment_id'}
  
  def post(self):
    return {'data2':'post assessment object'}
  
  def put(self):
    return {'data3':'assessment updated'}
  
  def delete(self):
    return {'data4':'deleted successfully'}
  
class AssessmentList(Resource):
  @jwt_required()
  def get(self):
    return {'assessments':'assessments list'}