from flask_jwt import jwt_required, current_identity
from flask_restful import Resource, fields, marshal_with, reqparse, abort
from sqlalchemy import extract
from db import session
from controllers.auth import checkadmin
from models import CourseModel, AssessmentModel
from marshal_base_fields import class_fields, faculty_fields

class_extra_fields = {
  'faculty': fields.Nested(faculty_fields),
  'completion': fields.Boolean,
  'total_students': fields.Integer(attribute=lambda x: len(x.students)),
  'total_completed_students': fields.Integer(attribute=lambda x: x.assessments_count / len(x.assigned_slos))
}

parser = reqparse.RequestParser()
parser.add_argument('year', default=None, type=str, required=False, location="args", help='Year option must be a valid 4 digit year')

class Progress(Resource):
    @jwt_required()
    @checkadmin
    @marshal_with({**class_fields, **class_extra_fields})
    def get(self):
      args = parser.parse_args()
      if args['year'] and (len(args['year']) != 4 or not args['year'].isdigit()):
        abort(422, message="year parameter must be a 4 digit year")
      
      if args['year']:
        courses = session.query(CourseModel).filter(extract('year', CourseModel.course_year) == args['year']).all()
      else:
        courses = session.query(CourseModel).all()
        
      return courses