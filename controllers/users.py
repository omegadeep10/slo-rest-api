from flask_jwt import jwt_required, current_identity
from flask_restful import Resource
from controllers.auth import checkadmin
from db import session
from models import User
import sys

class Users(Resource):
  @jwt_required()
  def get(self):
    return {'get user'}
  
  def put(self):
    return {'updated successfully'}