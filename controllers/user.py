from flask_jwt import jwt_required, current_identity
from flask_restful import Resource, fields, marshal_with, reqparse
from controllers.auth import checkadmin
from db import session
from marshal_base_fields import faculty_fields, class_fields


faculty_extra_fields = {
	'id': fields.Integer,
	'user_type': fields.String,
	'courses': fields.List(fields.Nested(class_fields))
}


class User(Resource):
	@jwt_required()
	@marshal_with({**faculty_fields, **faculty_extra_fields})
	def get(self):
		return current_identity # current_identity is the SQLAlchemy User Object