from flask_jwt import jwt_required, current_identity
from flask_restful import Resource, fields, marshal_with, abort, reqparse
from controllers.auth import checkadmin
from db import session
from models.User import UserModel
from datetime import datetime

user_fields = {
<<<<<<< HEAD
  'id': fields.String,
  'faculty_id': fields.String,
  'email': fields.String,
=======
  'email': fields.String,
  'faculty_id': fields.String,
>>>>>>> 2a1e112728e132056af16fd142338bb27649446a
  'first_name': fields.String,
  'last_name': fields.String,
  'user_type': fields.String
}

class Profile(Resource):
  @jwt_required()
  @marshal_with(user_fields)
  def get(self):
    return current_identity
<<<<<<< HEAD
  
  def put(self, crn):
    return {'data': 'profile updated successfully'}
    # To-Do => Parse arguments, update profile, return newly updated info to user
=======
  
>>>>>>> 2a1e112728e132056af16fd142338bb27649446a
