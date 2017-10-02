from flask_jwt import jwt_required, current_identity
from flask_restful import Resource, fields, marshal_with, abort, reqparse
from controllers.auth import checkadmin
from db import session
from models.User import UserModel
from datetime import datetime

user_fields = {
  'id': fields.String,
  'faculty_id': fields.String,
  'email': fields.String,
  'first_name': fields.String,
  'last_name': fields.String,
  'user_type': fields.String
}

class Profile(Resource):
  @jwt_required()
  @marshal_with(user_fields)
  def get(self):
    return current_identity
  
  def put(self, crn):
    return {'data': 'profile updated successfully'}
    # To-Do => Parse arguments, update profile, return newly updated info to user