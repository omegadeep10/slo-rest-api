from flask_jwt import jwt_required, current_identity
from flask_restful import Resource, fields, marshal_with, reqparse
from db import session
from models.Faculty import FacultyModel

user_fields = {
	'id': fields.Integer,
  'faculty_id': fields.String,
	'email': fields.String,
	'first_name': fields.String,
	'last_name': fields.String
}

parser = reqparse.RequestParser()
parser.add_argument('email', type=str, required = True, help='Email field is required.')
parser.add_argument('faculty_id', type=str, required = True, help='Email field is required.')
parser.add_argument('first_name', type=str, required = True, help='First Name field is required.')
parser.add_argument('last_name', type=str, required = True, help='Last Name field is required.')
parser.add_argument('password', type=str, required = True, help='Password field is required.')

class Register(Resource):
  @marshal_with(user_fields)
  def post(self):
    args = parser.parse_args()
    me = User(args['email'], args['faculty_id'], args['first_name'], args['last_name'], args['password'], userType='0') #usertype=0 is 'not admin'
    session.add(me)
    session.commit() #commits to a database
    return me