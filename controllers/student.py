from flask_jwt import jwt_required, current_identity
from flask_restful import Resource, reqparse, marshal_with, fields, abort
from controllers.auth import checkadmin
from db import session
from models import StudentModel, CourseModel, AssessmentModel
from marshal_base_fields import student_fields
import openpyxl
import base64
import sys
from io import StringIO, BytesIO

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
        
        # abort if not the course instructor
        if course.faculty.faculty_id != current_identity.faculty_id:
            abort(403, message="You are not authorized to add students to this course.")

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
            if student not in course.students: #If student is not ALREADY registered to course, add. Else just return
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
        # Abort if not course owner
        if course.faculty.faculty_id != current_identity.faculty_id:
            abort(403, message="You are not authorized to delete students from this course.")
        
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

batch_parser = reqparse.RequestParser()
batch_parser.add_argument('file', type=str, required = True, help='file is required and must be a valid excel spreadsheet.')

class BatchStudent(Resource):
    method_decorators = [jwt_required(), marshal_with({**student_fields, **student_detailed_fields})]

    def post(self, crn):
        args = batch_parser.parse_args()
        if not args['file'] or len(args['file'].encode('utf-8'))/1024 > 500:
            abort(422, message="File must be less than 500 Kb.")
        
        # Read b64 encoded data as binary file
        file_binary = base64.b64decode(args['file'])
        file_obj = BytesIO(file_binary)

        # open workbook
        wb = openpyxl.load_workbook(file_obj)
        ws1 = wb.worksheets[0]
        
        # load rows
        rows = []
        for row in ws1.rows:
            rows.append(row)
        
        # ensure file is not empty, or empty with just a header row
        if (len(rows) == 0) or (len(rows[1:]) == 0):
            abort(422, message="Excel file is empty.")
        
        # loop through and validate each row as a student. Add to list if valid
        valid_students = []
        for i, row in enumerate(rows[1:]):
            if isValidStudentID(str(row[0].value)) and isValidName(row[1].value) and isValidName(row[2].value):
                valid_students.append([str(row[0].value), row[1].value, row[2].value])
            else:
                abort(422, message="Invalid row {}. Student ID must be 9 digits, first and last name must be less than 255 chars.".format(i + 2))
        
        # ensure course exists and requester is authorized to add students to it
        course = session.query(CourseModel).filter(CourseModel.crn == crn).one_or_none() #queries the db for the course
        if not course: abort(404, message="requested course was not found")
        if course.faculty.faculty_id != current_identity.faculty_id:
            abort(403, message="You are not authorized to batch add students to this course.")
        
        # Add the valid students to the db
        for student in valid_students:
            studentObj = session.query(StudentModel).filter(StudentModel.student_id == student[0]).first() #queries the db for student using input
            if studentObj:
                #if student_id already exists, overwrite first_name and last_name
                studentObj.first_name = student[1]
                studentObj.last_name = student[2]
                session.add(studentObj) #pushes changes
            if not studentObj: #if student doesn't exist, it adds the student to the student table
                studentObj = StudentModel(student[0], student[1], student[2]) #puts this in db
                session.add(studentObj) #adds the info
            if studentObj not in course.students: #If student is not ALREADY registered to course, add. Else just return
                course.students.append(studentObj) #adds student to the course

        session.commit()
        return course.students


def isValidStudentID(student_id):
    if (isinstance(student_id, str) and len(student_id) == 9 and student_id.isdigit()):
        return True
    else:
        return False


def isValidName(name):
    if isinstance(name, str) and len(name) <= 255:
        return True
    else:
        return False
