from flask_jwt import jwt_required, current_identity
from flask_restful import Resource, reqparse, marshal_with, fields, abort
from controllers.auth import checkadmin
from db import session
from models import SLOModel, AssessmentModel, AssignedSLOModel, PerfIndicatorModel
from marshal_base_fields import slo_fields, performance_indicator_fields, class_fields
import re, sys


slo_detailed_fields = {
    'performance_indicators': fields.List(fields.Nested(performance_indicator_fields)),
    'courses': fields.List(fields.Nested({'crn': fields.String(attribute='course.crn')}))
}

slo_total_pi_fields = {
    'total_performance_indicators': fields.Integer(attribute=lambda x: len(x.performance_indicators))
}

def perfList(performance_indicator):
  if 'performance_indicator_id' not in performance_indicator or 'performance_indicator_description' not in performance_indicator:
    raise ValueError("All perfcormance indicators must contain a performance_indicator_id and a performance_indicator_description.")

  return performance_indicator

pi_id_match = re.compile('^[0-9][0-9]-[0-9][0-9]', re.IGNORECASE)
def fullPerfList(performance_indicator):
    if ('performance_indicator_id' not in performance_indicator or
        'performance_indicator_description' not in performance_indicator or
        'unsatisfactory_description' not in performance_indicator or
        'developing_description' not in performance_indicator or
        'satisfactory_description' not in performance_indicator or
        'exemplary_description' not in performance_indicator):
        raise ValueError("Invalid Performance Indicator object. Missing key:value pairs.")
    
    if (len(performance_indicator['performance_indicator_id']) != 5 or not pi_id_match.search(performance_indicator['performance_indicator_id'])):
        raise ValueError("Invalid performance_indicator_id")
    
    return performance_indicator


parser = reqparse.RequestParser()
parser.add_argument('slo_description', type=str, required = True, help='SLO description field is required.')
parser.add_argument('performance_indicators', type=perfList, required = True, help='Valid performance indicators are required.', action='append')


fullSLOParser = reqparse.RequestParser()
fullSLOParser.add_argument('slo_id', type=str, required = True, help='slo_id is required')
fullSLOParser.add_argument('slo_description', type=str, required = True, help='slo_description is required')
fullSLOParser.add_argument('performance_indicators', type=fullPerfList, required = True, help='Valid performance indicators required', action='append')

class SLO(Resource):
    @jwt_required()
    @marshal_with({**slo_fields, **slo_detailed_fields})
    def get(self, slo_id):
        slo = session.query(SLOModel).filter(SLOModel.slo_id == slo_id).first()
        if not slo: abort(404, message="SLO with the slo_id {} doesn't exist".format(slo_id))

        return slo
    
    @jwt_required()
    @checkadmin
    @marshal_with({**slo_fields, **slo_detailed_fields})
    def put(self, slo_id):
        args = fullSLOParser.parse_args()
        
        slo = session.query(SLOModel).filter(SLOModel.slo_id == slo_id).first()
        if not slo: abort(404, message="SLO with the slo_id {} doesn't exist".format(slo_id)) 

        perf_model_list = []
        for pi in args['performance_indicators']:
            perf = PerfIndicatorModel(pi['performance_indicator_id'], slo_id, pi['performance_indicator_description'], pi['unsatisfactory_description'], pi['developing_description'], pi['satisfactory_description'], pi['exemplary_description'])
            perf_model_list.append(perf)
        
        for pi in slo.performance_indicators:
            session.delete(pi)
        
        slo.slo_description = args['slo_description']
        slo.performance_indicators = perf_model_list
        session.commit()
        return slo

    @jwt_required()
    @checkadmin
    def delete(self,slo_id):
        assigned_slos = session.query(AssignedSLOModel).filter(AssignedSLOModel.slo_id == slo_id).all()
        assessments = session.query(AssessmentModel).filter(AssessmentModel.slo_id == slo_id).all()
        slo = session.query(SLOModel).filter(SLOModel.slo_id == slo_id).first()
        
        if not slo: abort(404, message="SLO with the slo_id {} doesn't exist".format(slo_id))
        if len(assigned_slos) > 0: abort(409, message="SLO cannot be deleted. Courses exist that are assigned to this SLO.") 
        if len(assessments) > 0: abort(409, message="SLO cannot be deleted. Assessments exist that reference it.")

        for pi in slo.performance_indicators:
            session.delete(pi)
        
        session.delete(slo)
        session.commit()
        return {}, 204 # Delete successful, so return empty 204 successful response


class SLOList(Resource):
    @jwt_required()
    @marshal_with({**slo_fields, **slo_total_pi_fields})
    def get(self):
        return session.query(SLOModel).all()
    

    @jwt_required()
    @checkadmin
    @marshal_with({**slo_fields, **slo_detailed_fields})
    def post(self):
        args = fullSLOParser.parse_args()

        existing_slo = session.query(SLOModel).filter(SLOModel.slo_id == args['slo_id']).first()
        if existing_slo: abort(409, message="SLO with the slo_id {} already exists.".format(args['slo_id']))

        slo = SLOModel(args['slo_id'], args['slo_description'])
        session.add(slo)

        perf_model_list = []
        for pi in args['performance_indicators']:
            if pi['performance_indicator_id'][:2] != args['slo_id']: abort(400, message="performance indicator ids MUST begin with the slo_id followed by a dash.")
            perf = PerfIndicatorModel(pi['performance_indicator_id'], args['slo_id'], pi['performance_indicator_description'], pi['unsatisfactory_description'], pi['developing_description'], pi['satisfactory_description'], pi['exemplary_description'])
            perf_model_list.append(perf)
        
        slo.performance_indicators = perf_model_list
        session.commit()
        return slo