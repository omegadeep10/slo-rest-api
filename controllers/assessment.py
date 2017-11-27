from flask_jwt import jwt_required, current_identity
from flask_restful import Resource, reqparse, marshal_with, fields, abort
from controllers.auth import checkadmin
from db import session
from models import AssessmentModel, CourseModel, PerfIndicatorModel, StudentModel, SLOModel, ScoreModel
from marshal_base_fields import student_fields, class_fields, slo_fields, score_fields
import sys
from functools import reduce

assessment_fields = {
  'assessment_id': fields.Integer,
  'total_score': fields.Integer,
  'student': fields.Nested(student_fields),
  'course': fields.Nested(class_fields),
  'slo': fields.Nested(slo_fields),
  'scores': fields.List(fields.Nested(score_fields))
}

def scoresList(score):
  if 'performance_indicator_id' not in score or 'score' not in score:
    raise ValueError("All scores must contain a performance_indicator_id and a score")
  
  if score['score'] < 1 or score['score'] > 4:
    raise ValueError("Score must be between 1 and 4")

  return score

parser = reqparse.RequestParser()
parser.add_argument('slo_id', type=str, required = True, help='SLO ID field is required.')
parser.add_argument('student_id', type=str, required = True, help='Total Score is required.')
parser.add_argument('scores', type=scoresList, required = True, help='Valid scores are required.', action='append')

putParser = reqparse.RequestParser()
putParser.add_argument('scores', type=scoresList, required = True, help='Valid scores are required', action='append')

class Assessment(Resource):
  method_decorators = [jwt_required()]

  @marshal_with(assessment_fields)
  def get(self, assessment_id):
    assessment = session.query(AssessmentModel).filter(AssessmentModel.assessment_id == assessment_id).first()

    if not assessment: abort(404, message="Assessment doesn't exist")
    
    # Ensure requester is authorized to view said assessment
    if (assessment.course.faculty.faculty_id != current_identity.faculty_id) and (current_identity.user_type != "1"):
      abort(403, message="You are not authorized to view this assessment.")

    return assessment
  
  @marshal_with(assessment_fields)
  def put(self, assessment_id):
    args = putParser.parse_args()

    assessment = session.query(AssessmentModel).filter(AssessmentModel.assessment_id == assessment_id).first()
    if not assessment: abort(404, message="Assessment doesn't exist") 

    if (assessment.course.faculty.faculty_id != current_identity.faculty_id):
      abort(403, message="You are not authorized to update this assessment.")

    total_score = reduce((lambda total, scoreObj: total + scoreObj['score']), [0] + args['scores']) # a fancy for loop with an accumulator
    assessment.total_score = total_score

    for score in args['scores']:
      for db_score in assessment.scores:
        if (db_score.performance_indicator_id == score['performance_indicator_id']):
          db_score.score = score['score']

    session.commit()
    return assessment
  
  def delete(self, assessment_id):
    assessment = session.query(AssessmentModel).filter(AssessmentModel.assessment_id == assessment_id).first()
    if (assessment):
      
      # Ensure requester is authorized to delete this assessment
      if (assessment.course.faculty.faculty_id != current_identity.faculty_id):
        abort(403, message="You are not authorized to delete this assessment.")

      for each_score in assessment.scores:
        session.delete(each_score)
      
      session.delete(assessment)
      session.commit()
      return {}, 204 # Delete successful, so return empty 204 successful response
    else:
      abort(404, message="Assessment with the assessment ID {} doesn't exist".format(assessment_id)) 


class AssessmentList(Resource):
  method_decorators = [jwt_required()]

  @marshal_with(assessment_fields)
  def get(self, crn):
    return session.query(AssessmentModel).filter(AssessmentModel.crn == crn).all()
  

  @marshal_with(assessment_fields)
  def post(self, crn):
    args = parser.parse_args()
    
    course = session.query(CourseModel).filter(CourseModel.crn == crn).one_or_none()
    slo = session.query(SLOModel).filter(SLOModel.slo_id == args['slo_id']).one_or_none()
    student = session.query(StudentModel).filter(StudentModel.student_id == args['student_id']).one_or_none()

    if not course: abort(404, message="Course doesn't exist.")
    if not slo: abort(404, message="SLO doesn't exist.")
    if not student: abort(404, message="Student doesn't exist")

    if course.faculty.faculty_id != current_identity.faculty_id:
      abort(403, message="You are not authorized to create new assessments for this course.")

    total_score = reduce((lambda total, scoreObj: total + scoreObj['score']), [0] + args['scores']) # a fancy for loop with an accumulator
    filed_assessment = AssessmentModel(crn, args['slo_id'], args['student_id'], total_score) # init our new assessment object
    session.add(filed_assessment) # add to the db (populates it with an assessment_id as well)

    scores_as_objs = []
    for score in args['scores']:
      perf_indicator = session.query(PerfIndicatorModel).filter(
        PerfIndicatorModel.performance_indicator_id == score['performance_indicator_id'],
        PerfIndicatorModel.slo_id == args['slo_id']
      ).one_or_none()
      
      if perf_indicator:
        scores_as_objs.append(ScoreModel(score['performance_indicator_id'], filed_assessment.assessment_id, score['score']))
      else:
        abort(500, message="Performance indicator with the id " + score['performance_indicator_id'] + " doesn't exist.")
    
    filed_assessment.scores = scores_as_objs

    session.commit()
    return filed_assessment