from flask_jwt import jwt_required, current_identity
from flask_restful import Resource
from controllers.auth import checkadmin
from db import session
from models import User
import sys

class Classes(Resource):
  @jwt_required()
  def get(self):
    return {'data':'get classes'}
  
  def get_crn(self):
    return {'data1':'get crn'}
  
  def post(self):
    return {'data2':'new crn'}
  
  def put(self):
    return {'data3':'edited successfully'}
  
  def delete(self):
    return {'data4':'deleted successfully'}