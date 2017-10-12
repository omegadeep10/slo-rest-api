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
    'courses': fields.List(fields.Nested(course_fields))
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
        args = parser.parse_args() #gets the input
        student = session.query(StudentModel).filter(StudentModel.student_id == args['student_id']).first() #queries the db for student using input
        course = session.query(CourseModel).filter(CourseModel.crn == args['crn']).one_or_none() #queries the db for the course
        if not student: #if student doesn't exist, it adds the student to the student table
            student = StudentModel(args['student_id'],args['first_name'],args['last_name']) #puts this in db
        if course: #if course exists, it adds info to the db
            session.add(student) #adds the info
            course.students.append(student) #adds student to the course
            session.commit() #commits it to db
            return student 
        else: #if course doesn't exist
            abort(404, message='Course does not exist.')