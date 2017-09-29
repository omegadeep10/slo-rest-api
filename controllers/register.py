from flask_jwt import jwt_required, current_identity
from flask_restful import Resource, fields, marshal_with, reqparse
from db import session
from user import User
import sys

user_fields = {
	'id': fields.Integer,
	'email': fields.String,
	'fname': fields.String,
	'lname': fields.String
}

class Register(Resource):
  @marshal_with(user_fields)
  def post(self):
    parser = reqparse.RequestParser()
    parser.add_argument('email',type=str,required = True, help='Email field is required.')
    parser.add_argument('fname',type=str,required = True, help='First Name field is required.')
    parser.add_argument('lname',type=str,required = True,help='Last Name field is required.')
    parser.add_argument('password',type=str,required = True,help='Password field is required.')
    args = parser.parse_args()
    me = User(args['email'],args['fname'],args['lname'],args['password'],userType='0') #usertype=0 is 'not admin'
    session.add(me)
    session.commit() #commits to a database
    return me