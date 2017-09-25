from flask_jwt import jwt_required, current_identity
from flask_restful import Resource
from controllers.auth import checkadmin
from db import session
from models import User
import sys

class Assessments(Resource):
  @jwt_required()
  def get(self):
    return {'data':'get assessments'}
  
  def get_assessment(self):
    return {'data1':'get assessment'}
  
  def post(self):
    return {'data2':'post assessment object'}
  
  def put(self):
    return {'data3':'assessment updated'}
  
  def delete(self):
    return {'data4':'deleted successfully'}