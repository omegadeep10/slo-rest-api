from flask_jwt import jwt_required, current_identity
from flask_restful import Resource, fields, marshal_with, reqparse
from db import session
from controllers.auth import checkadmin
from models import CourseModel, AssessmentModel
from marshal_base_fields import class_fields, faculty_fields

class_extra_fields = {
  'faculty': fields.Nested(faculty_fields),
  'completion': fields.Boolean 
}

class Progress(Resource):
    @jwt_required()
    @checkadmin
    @marshal_with({**class_fields, **class_extra_fields})
    def get(self):
        courses = session.query(CourseModel).all()
        return courses