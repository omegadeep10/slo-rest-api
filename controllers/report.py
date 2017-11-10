from flask_jwt import jwt_required, current_identity
from flask_restful import Resource, reqparse, marshal_with, fields, abort
from controllers.auth import checkadmin
from db import session
import xlsxwriter
import os, time
from sqlalchemy import extract
from models import AssessmentModel, PerfIndicatorModel, ScoreModel, CourseModel, SLOModel

def getScoreCount(ListOfAssessments, desiredScore, performanceIndicatorId):
    # scores => should be a list of score objects
    # desiredScore => 1, 2, 3, or 4
    count = 0

    for assessment in ListOfAssessments:
        for score in assessment.scores:
            if (score.performance_indicator_id == performanceIndicatorId) and (score.score == desiredScore):
                count = count + 1
    
    return count

def safeDivision(x, y):
    return 0 if x == 0 else x / y

def generateRawSLOData(excelWorkbook, slo, year):
    bold_format = excelWorkbook.add_format({'bold': True})
    percentage_format = excelWorkbook.add_format({'num_format': '0.0%'})

    worksheet = excelWorkbook.add_worksheet("SLO " + slo.slo_id) #adds a worksheet to the workbook
    row, column = 0, 0
    
    if year:
        assessments = session.query(AssessmentModel).join(AssessmentModel.course).\
        filter(AssessmentModel.slo_id == slo.slo_id, extract('year', CourseModel.course_year) == year).\
        order_by(AssessmentModel.crn).all()
    else:
        assessments = session.query(AssessmentModel).filter(AssessmentModel.slo_id == slo.slo_id).order_by(AssessmentModel.crn).all() #queries the tables for information

    # SLO Id top left, SLO description right next to it
    worksheet.write(row, column, "SLO " + slo.slo_id, bold_format) #adds data to the worksheet going by row and column numbers then the actual data
    worksheet.write(row, column + 1, slo.slo_description)
    
    row = row + 1
    # Generate PI id => description mapping table
    for performance_indicator in slo.performance_indicators:
        worksheet.write(row, column, performance_indicator.performance_indicator_id, bold_format)
        worksheet.write(row, column + 1, performance_indicator.performance_indicator_description)
        row = row + 1
    
    row = row + 1
    
    # worksheet.write(row, column, 'Student') # Decided against "Student in top left"
    column = column + 1
    # generate header row (Student, PI 1, PI 2, etc.)
    for performance_indicator in slo.performance_indicators:
        worksheet.write(row, column, performance_indicator.performance_indicator_id, bold_format)
        column = column + 1
    
    row = row + 1
    column = 0

    # Output data below the header (Student_id, score for PI 1, Score for PI 2, Score for PI 3)
    for assessment in assessments:
        worksheet.write(row, column, assessment.crn + " : " + assessment.student_id + " " + assessment.student.last_name + ", " + assessment.student.first_name)
        column = column + 1

        for score in assessment.scores:
            worksheet.write(row, column, score.score)
            column = column + 1
        
        column = 0
        row = row + 1

    # Empty row between raw data and summary statistics
    row = row + 1
    column = 0

    # Header row for Summary data
    # worksheet.write(row, column, 'Number of students who scored...') # Decided against this
    column = column + 1

    for performance_indicator in slo.performance_indicators:
        worksheet.write(row, column, performance_indicator.performance_indicator_id, bold_format)
        column = column + 1
    
    row = row + 1
    column = 0

    # Summary data
    for scoreRating in ([4, 'Exemplary'], [3, 'Satisfactory'], [2, 'Developing'], [1, 'Unsatisfactory']):
        worksheet.write(row, column, scoreRating[1], bold_format)
        column = column + 1
        
        for performance_indicator in slo.performance_indicators:
            worksheet.write(row, column, getScoreCount(assessments, scoreRating[0], performance_indicator.performance_indicator_id))
            column = column + 1
        
        row = row + 1
        column = 0
    
    # Empty row between summary and totals
    row = row + 1

    # Totals for Summary
    worksheet.write(row, column, 'Total')
    column = column + 1

    for performance_indicator in slo.performance_indicators:
        worksheet.write(row, column, len(assessments))
        column = column + 1
    
    row = row + 1
    column = 0

    worksheet.write(row, column, 'Percent who scored either Satisfactory or Exemplary')
    column = column + 1

    for performance_indicator in slo.performance_indicators:

        percentForExemplary = safeDivision(getScoreCount(assessments, 4, performance_indicator.performance_indicator_id), len(assessments))
        percentForSatisfactory = safeDivision(getScoreCount(assessments, 3, performance_indicator.performance_indicator_id), len(assessments))
        worksheet.write(row, column, (percentForExemplary + percentForSatisfactory), percentage_format)
        column = column + 1


    # Two empty rows for separation between classes
    row = row + 3
    column = 0

# Responsible for generating first sheet and populating with raw user data
def generateRawCourseData(excelWorkbook, course):
    bold_format = excelWorkbook.add_format({'bold': True})
    percentage_format = excelWorkbook.add_format({'num_format': '0.0%'})

    worksheet = excelWorkbook.add_worksheet(course.course_type + " " + course.course_number + " - " + course.crn) #adds a worksheet to the workbook
    row, column = 0, 0
    
    for assignedSlo in course.assigned_slos:
        assessments = session.query(AssessmentModel).filter(AssessmentModel.crn == course.crn, AssessmentModel.slo_id == assignedSlo.slo_id).all() #queries the tables for information

        # CRN top left, SLO description right next to it
        worksheet.write(row, column, "ITEC " + course.course_number, bold_format) #adds data to the worksheet going by row and column numbers then the actual data
        worksheet.write(row, column + 1, course.course_type)
        worksheet.write(row, column + 2, course.crn)
        worksheet.write(row, column + 3, course.course_year.year)
        worksheet.write(row, column + 4, assignedSlo.slo_id + " : " + assignedSlo.slo.slo_description)
        
        # generate header row (Student, PI 1, PI 2, etc.)
        row = row + 1
        # worksheet.write(row, column, 'Student') # Decided against "Student in top left"
        column = column + 1

        for performance_indicator in assignedSlo.slo.performance_indicators:
            worksheet.write(row, column, performance_indicator.performance_indicator_description, bold_format)
            column = column + 1
        
        row = row + 1
        column = 0

        # Output data below the header (Student_id, score for PI 1, Score for PI 2, Score for PI 3)
        for assessment in assessments:
            worksheet.write(row, column, assessment.student_id + " " + assessment.student.last_name + ", " + assessment.student.first_name)
            column = column + 1

            for score in assessment.scores:
                worksheet.write(row, column, score.score)
                column = column + 1
            
            column = 0
            row = row + 1

        # Empty row between raw data and summary statistics
        row = row + 1
        column = 0

        # Header row for Summary data
        # worksheet.write(row, column, 'Number of students who scored...') # Decided against this
        column = column + 1

        for performance_indicator in assignedSlo.slo.performance_indicators:
            worksheet.write(row, column, performance_indicator.performance_indicator_description, bold_format)
            column = column + 1
        
        row = row + 1
        column = 0

        # Summary data
        for scoreRating in ([4, 'Exemplary'], [3, 'Satisfactory'], [2, 'Developing'], [1, 'Unsatisfactory']):
            worksheet.write(row, column, scoreRating[1], bold_format)
            column = column + 1
            
            for performance_indicator in assignedSlo.slo.performance_indicators:
                worksheet.write(row, column, getScoreCount(assessments, scoreRating[0], performance_indicator.performance_indicator_id))
                column = column + 1
            
            row = row + 1
            column = 0
        
        # Empty row between summary and totals
        row = row + 1

        # Totals for Summary
        worksheet.write(row, column, 'Total')
        column = column + 1

        for performance_indicator in assignedSlo.slo.performance_indicators:
            worksheet.write(row, column, len(assessments))
            column = column + 1
        
        row = row + 1
        column = 0

        worksheet.write(row, column, 'Percent who scored either Satisfactory or Exemplary')
        column = column + 1

        for performance_indicator in assignedSlo.slo.performance_indicators:

            percentForExemplary = safeDivision(getScoreCount(assessments, 4, performance_indicator.performance_indicator_id), len(assessments))
            percentForSatisfactory = safeDivision(getScoreCount(assessments, 3, performance_indicator.performance_indicator_id), len(assessments))
            worksheet.write(row, column, (percentForExemplary + percentForSatisfactory), percentage_format)
            column = column + 1


        # Two empty rows for separation between classes
        row = row + 3
        column = 0


def cleanup(directory):
    now = time.time()
    old = now - (7 * 24 * 60 * 60) # delete all reports older than one week

    for f in os.listdir(directory):
        path = os.path.join(directory, f)
        if (os.path.isfile(path)):
            stat = os.stat(path)
            if stat.st_ctime < old:
                os.remove(path)


parser = reqparse.RequestParser()
parser.add_argument('year', default=None, type=str, required=False, location="args", help='Year option must be a valid 4 digit year')

# => /reports/courses?year=2017 TO-DO Add optional year filtering
class CourseReports(Resource):
    @jwt_required()
    @checkadmin
    def get(self):
        args = parser.parse_args()
        if (args['year'] and len(args['year']) != 4 and not args['year'].isdigit()):
            abort(422, message="year parameter must be a 4 digit year")
        
        if (args['year']):
            courses = session.query(CourseModel).filter(extract('year', CourseModel.course_year) == args['year']).all()
        else:
            courses = session.query(CourseModel).all()

        cleanup('static')

        # Generate workbook
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        workbook = xlsxwriter.Workbook('static/slos-export-' + timestamp + '.xlsx') #creates the workbook and names it
        for course in courses:
            generateRawCourseData(workbook, course)

        workbook.close() #closes the workbook

        return { 'file_url': '/static/slos-export-'+ timestamp + '.xlsx' }, 200


# => /reports/slos?year=2017 TO-DO Add optional year filtering
class SLOReports(Resource):
    @jwt_required()
    @checkadmin
    def get(self):
        args = parser.parse_args()
        if (args['year'] and len(args['year']) != 4 and not args['year'].isdigit()):
            abort(422, message="year parameter must be a 4 digit year")

        slos = session.query(SLOModel).all()
        cleanup('static')

        timestamp = time.strftime("%Y%m%d-%H%M%S")
        workbook = xlsxwriter.Workbook('static/slos-export-' + timestamp + '.xlsx') #creates the workbook and names it
        
        for slo in slos:
            generateRawSLOData(workbook, slo, args['year'])
        
        workbook.close()

        return { 'file_url': '/static/slos-export-'+ timestamp + '.xlsx' }, 200