from flask_jwt import jwt_required, current_identity
from flask_restful import Resource, fields, marshal_with, reqparse
from controllers.auth import checkadmin
from db import session
from models import CourseModel, AssessmentModel
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

class_data_fields = {
    'crn': fields.String,
    'course_name': fields.String,
    'course_type': fields.String,
    'semester': fields.String,
    'course_year': fields.String(attribute=lambda x: x['course_year'].year), # extract only the Year as a string
    'total_students': fields.Integer,
    'assigned_slos': fields.List(fields.Nested(slo_data_fields)),
    'completion': fields.Boolean
}

# Input: List of AssessmentModel objects, AssignedSLO object
# Output: List of PI data in the format specified by pi_data_fields
def generateSummaryData(listOfAssessments, assignedSLO):
    summaryData = [] #container
    relevant_assessments = [x for x in listOfAssessments if x.slo_id == assignedSLO.slo_id] # Filters assessments to just be the ones for this specific SLO
    relevant_scores = [] #container that will hold all scores

    # For each relevant assessment, add it's scores to the relevant_scores container
    for a in relevant_assessments: relevant_scores = relevant_scores + a.scores

    for pi in assignedSLO.slo.performance_indicators:
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

class CourseDataList(Resource):
    
    @jwt_required()
    @checkadmin
    @marshal_with(class_data_fields)
    def get(self):
        course_data_formatted = []
        courses = session.query(CourseModel).all()
        
        for course in courses:
            course_assessments = session.query(AssessmentModel).filter(AssessmentModel.crn == course.crn).all()

            course_data = {
                'crn': course.crn,
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
                    'performance_indicators': generateSummaryData(course_assessments, slo)
                })
            
            course_data_formatted.append(course_data)
        
        return course_data_formatted