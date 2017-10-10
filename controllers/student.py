from flask_jwt import jwt_required, current_identity
from flask_restful import Resource, reqparse, marshal_with, fields, abort
from controllers.auth import checkadmin
from db import session
from models import StudentModel
from models import registration

parser = reqparse.RequestParser()
parser.add_argument('student_id', type=str, required = True, help='Email field is required.')
parser.add_argument('first_name', type=str, required = True, help='Student First Name field is required.')
parser.add_argument('last_name', type=str, required = True, help='Last Name field is required.')
parser.add_argument('crn', type=str, required = True, help='CRN field is required.')

class Student(Resource):
    @jwt_required()
    def post(self):
        args = parser.parse_args()