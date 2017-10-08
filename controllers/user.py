from flask_jwt import jwt_required, current_identity
from flask_restful import Resource, fields, marshal_with, reqparse
from controllers.auth import checkadmin
from db import session

class_fields = {
	'crn': fields.String,
	'course_name': fields.String,
	'course_type': fields.String,
	'semester': fields.String,
	'course_year': fields.String(attribute=lambda x: x.course_year.year), # extract only the Year as a string
}

user_fields = {
	'id': fields.Integer,
	'email': fields.String,
	'faculty_id': fields.String,
	'first_name': fields.String,
	'last_name': fields.String,
	'user_type': fields.String,
	'courses': fields.List(fields.Nested(class_fields))
}


class User(Resource):
	@jwt_required()
	@marshal_with(user_fields)
	def get(self):
		return current_identity # current_identity is the SQLAlchemy User Object