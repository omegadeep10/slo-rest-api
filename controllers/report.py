from flask_jwt import jwt_required, current_identity
from flask_restful import Resource, reqparse, marshal_with, fields, abort
from controllers.auth import checkadmin
from db import session
import xlsxwriter
from models import AssessmentModel, PerfIndicatorModel, ScoreModel, SLOModel

class Report(Resource):

    def get(self,crn):
        assessment = session.query(AssessmentModel).filter(AssessmentModel.crn == crn).first() #queries the tables for information
        slos = session.query(SLOModel).filter(SLOModel.slo_id == assessment.slo_id).first()
        scores = session.query(ScoreModel).filter(ScoreModel.assessment_id == AssessmentModel.assessment_id).first()

        workbook = xlsxwriter.Workbook('slos.xlsx') #creates the workbook and names it
        worksheet = workbook.add_worksheet('SLOS') #adds a worksheet to the workbook

        indicators = [] #intliazes a list
        for performance_indicator in slos.performance_indicators: 
            indicators.append(performance_indicator)  #loops through each performance indicator and adds it to the list

        worksheet.write(0, 0, 'CRN') #adds data to the worksheet going by row and column numbers then the actual data
        worksheet.write(0, 1, 'Student ID')
        worksheet.write(0, 2, 'SLO ID')
        worksheet.write(0, 3, "SLO Description")
        worksheet.write(0, 4, 'Performance Indicator')
        worksheet.write(0, 5, 'Score')
        worksheet.write(1, 0, assessment.crn)
        worksheet.write(1, 1, assessment.student_id)
        worksheet.write(1, 2, assessment.slo_id)
        worksheet.write(1, 3, assessment.slo.slo_description)
        worksheet.write(1, 4, indicators[0].performance_indicator_description)
        worksheet.write(1, 5, scores.score)

        workbook.close() #closes the workbook