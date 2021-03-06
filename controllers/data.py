from flask_jwt import jwt_required, current_identity
from flask_restful import Resource, fields, marshal_with, reqparse, abort
from sqlalchemy import extract
from controllers.auth import checkadmin
from db import session
from models import CourseModel, AssessmentModel, SLOModel
from marshal_base_fields import class_fields, faculty_fields

pi_data_fields = {
    'performance_indicator_id': fields.String,
    'performance_indicator_description': fields.String,
    'unsatisfactory': fields.Integer,
    'developing': fields.Integer,
    'satisfactory': fields.Integer,
    'exemplary': fields.Integer
}

slo_data_fields = {
    'slo_id': fields.String,
    'slo_description': fields.String,
    'performance_indicators': fields.List(fields.Nested(pi_data_fields))
}

slo_data_extra_fields = {
    'total_assessments': fields.Integer
}

class_data_fields = {
    'crn': fields.String,
    'course_number': fields.String,
    'course_name': fields.String,
    'course_type': fields.String,
    'semester': fields.String,
    'course_year': fields.String(attribute=lambda x: x['course_year'].year), # extract only the Year as a string
    'total_students': fields.Integer,
    'assigned_slos': fields.List(fields.Nested(slo_data_fields)),
    'completion': fields.Boolean
}

# Input: List of AssessmentModel objects, SLO object
# Output: List of PI data in the format specified by pi_data_fields
def generateSummaryData(listOfAssessments, SLOModel):

    summaryData = [] #container
    relevant_assessments = [x for x in listOfAssessments if x.slo_id == SLOModel.slo_id] # Filters assessments to just be the ones for this specific SLO
    relevant_scores = [] #container that will hold all scores

    # For each relevant assessment, add it's scores to the relevant_scores container
    for a in relevant_assessments: relevant_scores = relevant_scores + a.scores

    for pi in SLOModel.performance_indicators:
        summaryData.append({
            'performance_indicator_id': pi.performance_indicator_id,
            'performance_indicator_description': pi.performance_indicator_description,
            # Counts the number of relevant scores for this specific performance_indicator where the score is 1, 2, 3, 4, etc.
            'unsatisfactory': len([x for x in relevant_scores if x.performance_indicator_id == pi.performance_indicator_id and x.score == 1]),
            'developing': len([x for x in relevant_scores if x.performance_indicator_id == pi.performance_indicator_id and x.score == 2]),
            'satisfactory': len([x for x in relevant_scores if x.performance_indicator_id == pi.performance_indicator_id and x.score == 3]),
            'exemplary': len([x for x in relevant_scores if x.performance_indicator_id == pi.performance_indicator_id and x.score == 4])
        })
    
    return summaryData

parser = reqparse.RequestParser()
parser.add_argument('filter_by', default=None, type=str, required=False, location="args", help='Filter option must be ONLINE or F2F')
parser.add_argument('year', default=None, type=str, required=False, location="args", help='Year option must be a valid 4 digit year')

class SLODataList(Resource):
    @jwt_required()
    @checkadmin
    @marshal_with({**slo_data_fields, **slo_data_extra_fields})
    def get(self, slo_id):
        args = parser.parse_args()
        if args['filter_by'] and (args['filter_by'] != 'ONLINE' and args['filter_by'] != 'F2F'):
            abort(422, message="filter_by parameter must be ONLINE or F2F")
        if (args['year'] and len(args['year']) != 4 and not args['year'].isdigit()):
            abort(422, message="year parameter must be a 4 digit year")

        slo = session.query(SLOModel).filter(SLOModel.slo_id == slo_id).first()
        if not slo: abort(404, message="SLO with the slo_id {} doesn't exist".format(slo_id))
        
        if args['filter_by'] and args['year']:
            slo_assessments = session.query(AssessmentModel).join(AssessmentModel.course).filter(
                AssessmentModel.slo_id == slo_id,
                CourseModel.course_type == args['filter_by'],
                extract('year', CourseModel.course_year) == args['year']
            ).all()
        elif args['filter_by']:
            slo_assessments = session.query(AssessmentModel).join(AssessmentModel.course).filter(AssessmentModel.slo_id == slo_id, CourseModel.course_type == args['filter_by']).all()
        elif args['year']:
            slo_assessments = session.query(AssessmentModel).join(AssessmentModel.course).filter(AssessmentModel.slo_id == slo_id, extract('year', CourseModel.course_year) == args['year']).all()
        else:
            slo_assessments = session.query(AssessmentModel).filter(AssessmentModel.slo_id == slo.slo_id).all()

        slo_data = {
            'slo_id': slo.slo_id,
            'slo_description': slo.slo_description,
            'total_assessments': len(slo_assessments),
            'performance_indicators': generateSummaryData(slo_assessments, slo)
        }
        
        return slo_data

class CourseDataList(Resource):
    
    @jwt_required()
    @checkadmin
    @marshal_with(class_data_fields)
    def get(self, crn):
        course = session.query(CourseModel).filter(CourseModel.crn == crn).first()
        course_assessments = session.query(AssessmentModel).filter(AssessmentModel.crn == course.crn).all()

        course_data = {
            'crn': course.crn,
            'course_number': course.course_number,
            'course_name': course.course_name,
            'course_type': course.course_type,
            'semester': course.semester,
            'course_year': course.course_year,
            'total_students': len(course.students),
            'assigned_slos': [],
            'completion': course.completion
        }

        for slo in course.assigned_slos:
            course_data['assigned_slos'].append({
                'slo_id': slo.slo_id,
                'slo_description': slo.slo.slo_description,
                'performance_indicators': generateSummaryData(course_assessments, slo.slo)
            })
        
        return course_data