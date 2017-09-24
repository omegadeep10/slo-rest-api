from flask_jwt import jwt_required, current_identity
from flask_restful import Resource, fields, marshal_with
from controllers.auth import checkadmin
from db import session
from models import User

user_fields = {
	'id': fields.Integer,
    'email': fields.String,
    'fname': fields.String,
    'lname': fields.String,
    'userType': fields.String
}

class User(Resource):
	@jwt_required()
	@marshal_with(user_fields)
	def get(self):
		return current_identity # current_identity is the SQLAlchemy User Object