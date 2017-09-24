from flask_jwt import jwt_required, current_identity
from flask_restful import Resource
from controllers.auth import checkadmin
from db import session
from models import User
import sys

class Classes(Resource):
  @jwt_required()
  def get(self):
    return {'get classes'}
  
  def get_crn(self):
    return {'get crn'}
  
  def post(self):
    return {'new crn'}
  
  def put(self):
    return {'edited successfully'}
  
  def delete(self):
    return {'deleted successfully'}