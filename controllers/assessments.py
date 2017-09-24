from flask_jwt import jwt_required, current_identity
from flask_restful import Resource
from controllers.auth import checkadmin
from db import session
from models import User
import sys

class Assessments(Resource):
  @jwt_required()
  def get(self):
    return {'get assessments'}
  
  def get_assessment(self):
    return {'get assessment'}
  
  def post(self):
    return {'post assessment object'}
  
  def put(self):
    return {'assessment updated'}
  
  def delete(self):
    return {'deleted successfully'}