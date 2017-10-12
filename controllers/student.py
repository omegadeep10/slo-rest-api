from flask_jwt import jwt_required, current_identity
from flask_restful import Resource, reqparse, marshal_with, fields, abort
from controllers.auth import checkadmin
from db import session
from models import StudentModel, CourseModel

course_fields = {
    'crn': fields.String,
    'course_name': fields.String
}

student_fields = {
	'student_id': fields.String,
	'first_name': fields.String,
	'last_name': fields.String,
    'courses': fields.Nested(course_fields)
}

parser = reqparse.RequestParser()
parser.add_argument('student_id', type=str, required = True, help='Email field is required.')
parser.add_argument('first_name', type=str, required = True, help='Student First Name field is required.')
parser.add_argument('last_name', type=str, required = True, help='Last Name field is required.')
parser.add_argument('crn', type=str, required = True, help='CRN field is required.')

class Student(Resource):
    @jwt_required()
    @marshal_with(student_fields)
    def post(self):
        args = parser.parse_args()
        student = StudentModel(args['student_id'],args['first_name'],args['last_name'])
        course = session.query(CourseModel).filter(CourseModel.crn == args['crn']).one_or_none()
        if course:
            session.add(student)
            course.students.append(student)
            student.courses
            session.commit()
        return session.query(StudentModel).filter(StudentModel.student_id == args['student_id']).first()
