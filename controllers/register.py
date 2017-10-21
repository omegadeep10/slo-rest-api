from flask_jwt import jwt_required, current_identity
from flask_restful import Resource, fields, marshal_with, reqparse, abort
from db import session
from models import FacultyModel
from marshal_base_fields import faculty_fields
import sys

parser = reqparse.RequestParser()
parser.add_argument('email', type=str, required = True, help='Email field is required.')
parser.add_argument('faculty_id', type=str, required = True, help='Faculty ID field is required.')
parser.add_argument('first_name', type=str, required = True, help='First Name field is required.')
parser.add_argument('last_name', type=str, required = True, help='Last Name field is required.')
parser.add_argument('password', type=str, required = True, help='Password field is required.')

class Register(Resource):
  @marshal_with(faculty_fields)
  def post(self):
    args = parser.parse_args()
    faculty =  session.query(FacultyModel).filter(FacultyModel.email == args['email']).one_or_none()
    me = FacultyModel(args['email'], args['faculty_id'], args['first_name'], args['last_name'], args['password'], user_type='0') #usertype=0 is 'not admin'
    if not faculty:
      session.add(me)
      session.commit() #commits to a database
      return me
    else:
      abort(404, message="Faculty members with this email already exists.")