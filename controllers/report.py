from flask_jwt import jwt_required, current_identity
from flask_restful import Resource, reqparse, marshal_with, fields, abort
from controllers.auth import checkadmin
from db import session
import xlsxwriter
import os
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

# Responsible for generating first sheet and populating with raw user data
def generateRawData(excelWorkbook, course):
    worksheet = excelWorkbook.add_worksheet('RawData') #adds a worksheet to the workbook
    row, column = 0, 0
    
    for assignedSlo in course.assigned_slos:
        assessments = session.query(AssessmentModel).filter(AssessmentModel.crn == course.crn, AssessmentModel.slo_id == assignedSlo.slo_id).all() #queries the tables for information

        # CRN top left, SLO description right next to it
        worksheet.write(row, column, course.crn) #adds data to the worksheet going by row and column numbers then the actual data
        worksheet.write(row, column + 1, assignedSlo.slo_id + " : " + assignedSlo.slo.slo_description)
        
        # generate header row (Student, PI 1, PI 2, etc.)
        row = row + 1
        worksheet.write(row, column, 'Student')
        column = column + 1

        for performance_indicator in assignedSlo.slo.performance_indicators:
            worksheet.write(row, column, performance_indicator.performance_indicator_description)
            column = column + 1
        
        row = row + 1
        column = 0

        # Output data below the header (Student_id, score for PI 1, Score for PI 2, Score for PI 3)
        for assessment in assessments:
            worksheet.write(row, column, assessment.student_id)
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
        worksheet.write(row, column, 'Number of students who scored...')
        column = column + 1

        for performance_indicator in assignedSlo.slo.performance_indicators:
            worksheet.write(row, column, performance_indicator.performance_indicator_description)
            column = column + 1
        
        row = row + 1
        column = 0

        # Summary data
        for scoreRating in ([4, 'Exemplary'], [3, 'Satisfactory'], [2, 'Developing'], [1, 'Unsatisfactory']):
            worksheet.write(row, column, scoreRating[1])
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
            worksheet.write(row, column, percentForExemplary + percentForSatisfactory)
            column = column + 1


        # Two empty rows for separation between classes
        row = row + 3
        column = 0


class Report(Resource):

    def get(self,crn):
        course = session.query(CourseModel).filter(CourseModel.crn == crn).one_or_none()

        # Remove the slos.xlsx file if it exists
        try:
            os.remove('static/slos.xlsx')
        except OSError:
            pass

        # Generate workbook
        workbook = xlsxwriter.Workbook('static/slos.xlsx') #creates the workbook and names it
        generateRawData(workbook, course)

        workbook.close() #closes the workbook

        return { 'file_url': 'https://slos.deeppatel.me/api/static/slos.xlsx' }, 200