from flask_jwt import jwt_required, current_identity
from flask_restful import Resource, reqparse, marshal_with, fields, abort
from controllers.auth import checkadmin
from db import session
from models import StudentModel, CourseModel, AssessmentModel
from marshal_base_fields import student_fields

course_fields = {
    'crn': fields.String,
    'course_name': fields.String
}

student_detailed_fields = {
    'courses': fields.List(fields.Nested(course_fields))
}

parser = reqparse.RequestParser()
parser.add_argument('first_name', type=str, required = True, help='Student First Name field is required.')
parser.add_argument('last_name', type=str, required = True, help='Last Name field is required.')
parser.add_argument('crn', type=str, required = True, help='CRN field is required.')

delete_parser = reqparse.RequestParser()

delete_parser.add_argument('crn', type=str, required = True, help='CRN field is required.')

class Student(Resource):
    method_decorators = [jwt_required(), marshal_with({**student_fields, **student_detailed_fields})]

    def get(self, student_id):
        return session.query(StudentModel).filter(StudentModel.student_id == student_id).first()

    def post(self, student_id):
        args = parser.parse_args() #gets the input
        student = session.query(StudentModel).filter(StudentModel.student_id == student_id).first() #queries the db for student using input
        course = session.query(CourseModel).filter(CourseModel.crn == args['crn']).one_or_none() #queries the db for the course
        if student:
            #if student_id already exists, overwrite first_name and last_name
            #student = StudentModel(student_id, args['first_name'], args['last_name'])
            student.first_name = args['first_name']
            student.last_name = args['last_name']
            session.add(student) #pushes changes
        if not student: #if student doesn't exist, it adds the student to the student table
            student = StudentModel(student_id, args['first_name'], args['last_name']) #puts this in db
            session.add(student) #adds the info
        if course: #if course exists, it adds info to the db
            course.students.append(student) #adds student to the course
            session.commit() #commits it to db
            return student
        else: #if course doesn't exist
            abort(404, message='Course does not exist.')

    def delete(self, student_id):
        args = delete_parser.parse_args() 
        student = session.query(StudentModel).filter(StudentModel.student_id == student_id).first()
        course = session.query(CourseModel).filter(CourseModel.crn == args['crn']).first()
        assessments = session.query(AssessmentModel).filter(AssessmentModel.crn == args['crn'], AssessmentModel.student_id == student_id).all()
        
        #remove student from the course
        #remove any assessments for that student for that course
        if student and course: #student and course must exist
            if student in course.students:
                course.students.remove(student)  
                for each_assessment in assessments:
                    for each_score in each_assessment.scores:
                        session.delete(each_score) #deletes the scores property for deletion
                    
                    session.delete(each_assessment) #loops and deletes each assessment
            session.commit()
            return {}, 204 #Delete successful
        else:
            abort(404, message = "Delete unsuccessful")