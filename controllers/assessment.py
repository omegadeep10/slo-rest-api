from flask_jwt import jwt_required, current_identity
from flask_restful import Resource, reqparse, marshal_with, fields, abort
from controllers.auth import checkadmin
from db import session
from models import AssessmentModel, ScoreModel, PerfIndicatorModel, CourseModel, StudentModel, SLOModel
import sys, pickle

parser = reqparse.RequestParser()
parser.add_argument('crn', type=str, required = True, help='Student ID field is required.')
parser.add_argument('slo_id', type=str, required = True, help='SLO ID field is required.')
parser.add_argument('student_id', type=str, required = True, help='Total Score is required.')
parser.add_argument('performance_indicator_id', type=str, required= True, help='Performance Indicator ID is required')
parser.add_argument('score', type=int, required= True, help='Score is required')

faculty_fields = {
	'faculty_id': fields.String,
	'first_name': fields.String,
	'last_name': fields.String
}

class_fields = {
  'crn': fields.String,
  'course_name': fields.String,
  'course_type': fields.String,
  'semester': fields.String,
  'course_year': fields.String(attribute=lambda x: x.course_year.year), # extract only the Year as a string
  # 'comments': fields.String, # Don't need comments
  # 'faculty': fields.Nested(faculty_fields) # Don't need faculty
}

student_fields = {
	'student_id': fields.String,
	'first_name': fields.String,
	'last_name': fields.String
}

slo_fields = {
	'slo_id': fields.String,
	'slo_description': fields.String
}

score_fields = {
  'performance_indicator_id': fields.String,
  'score': fields.Integer
}

assessment_fields = {
  'assessment_id': fields.Integer,
  'slo_id': fields.String,
  'total_score': fields.Integer,
  'student': fields.Nested(student_fields),
  'course': fields.Nested(class_fields),
  'slo': fields.Nested(slo_fields),
  'scores': fields.List(fields.Nested(score_fields))
}

class Assessment(Resource):
  @jwt_required()
  @marshal_with(assessment_fields)
  def get(self,assessment_id):
    return session.query(AssessmentModel).filter(AssessmentModel.assessment_id == assessment_id).first()
  
  def put(self):
    return {'data3':'assessment updated'}
  
  def delete(self):
    return {'data4':'deleted successfully'}
  
class AssessmentList(Resource):
  @jwt_required()
  @marshal_with(assessment_fields)
  def get(self, crn):
    return session.query(AssessmentModel).filter(AssessmentModel.crn == crn).all()

class NewAssessment(Resource):
  @jwt_required()
  @marshal_with(assessment_fields)
  def post(self):
    args = parser.parse_args()
    course = session.query(CourseModel).filter(CourseModel.crn == args['crn']).one_or_none()
    student = session.query(StudentModel).filter(StudentModel.student_id == args['student_id']).one_or_none()
    slo = session.query(SLOModel).filter(SLOModel.slo_id == args['slo_id']).one_or_none()
    performance_indicator = session.query(PerfIndicatorModel).filter(PerfIndicatorModel.slo_id == args['slo_id']).all()
    perfindicatorList = []
    argsList = []
    while args['performance_indicator_id'] != 0:
      argsList.append(args['performance_indicator_id'])
    while performance_indicator != 0:
      perfindicatorList.append(performance_indicator)
    assessment = AssessmentModel()
    score = ScoreModel(score = args['score'])
    score.PerfIndicatorModel = PerfIndicatorModel()
    if course:
      if student:
        if slo:
          if len(argsList) == len(perfindicatorList):
            scoreList = []
            while args['score'] != 0:
              scoreList.append(args['score'])
            for i in scoreList[i]:
              total_score += i
            newAssessment = AssessmentModel(args['crn'],args['slo_id'],args['student_id'],args['performance_indicator_id'],total_score)
            session.add(newAssessment)
            for i in scoreList[i]:
              score = i
              assessment.scores.append(score)
            session.commit()
            return newAssessment
          else:
            abort(404, message='The number of performance indicators does not match what is in the system.')
        else:
          abort(404, message='SLO does not exist.')
      else:
        abort(404, message='Student does not exist.')
    else:
      abort(404, message='Course does not exist.')