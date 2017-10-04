from flask_jwt import jwt_required, current_identity
from flask_restful import Resource, fields, marshal_with, reqparse
from controllers.auth import checkadmin
from db import session
from faculty import Faculty

user_fields = {
	'id': fields.Integer,
	'email': fields.String,
	'faculty_id': fields.String,
	'first_name': fields.String,
	'last_name': fields.String,
	'user_type': fields.String
}

class User(Resource):
	@jwt_required()
	@marshal_with(user_fields)
	def get(self):
		return current_identity # current_identity is the SQLAlchemy User Object