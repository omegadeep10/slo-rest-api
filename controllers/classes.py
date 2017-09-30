from flask_jwt import jwt_required, current_identity
from flask_restful import Resource, reqparse, marshal_with, fields
from controllers.auth import checkadmin
from db import session
from course import Course 
import sys
import datetime

class_fields = {
	'CRN': fields.String,
	'courseName': fields.String,
	'courseType': fields.String,
	'semester': fields.String,
	'courseYear': fields.String
}

class Classes(Resource):
  @jwt_required()
  def get(self,CRN):
    return {'data':'CRN'}
  
  def get_crn(self):
    return {'data1':'get crn'}
  
  def put(self):
    return {'data3':'edited successfully'}
  
  def delete(self):
    return {'data4':'deleted successfully'}
  
class ClassesList(Resource):
	@jwt_required()
	@marshal_with(class_fields)
	def get(self):
		parser = reqparse.RequestParser()
		parser.add_argument('CRN',type=str,required = True, help='CRN field is required.')
		args = parser.parse_args()
		class_CRN = args['CRN']
		return session.query(Course).filter(Course.CRN == class_CRN).one_or_none()
	
	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument('CRN',type=str,required = True, help='CRN field is required.')
		parser.add_argument('courseName',type=str,required = True, help='Course Name field is required.')
		parser.add_argument('courseType',type=str,required = True,help='Course Type field is required.')
		parser.add_argument('semester',type=str,required = True,help='Semester field is required.')
		parser.add_argument('courseYear',type=str,required = True,help='Course Year field is required.')
		args = parser.parse_args()
		me = Course(args['CRN'],args['courseName'],args['courseType'],args['semester'],args['courseYear'])
		session.add(me)
		session.commit() #commits to a database
		return me