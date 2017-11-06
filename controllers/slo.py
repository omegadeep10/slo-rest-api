from flask_jwt import jwt_required, current_identity
from flask_restful import Resource, reqparse, marshal_with, fields, abort
from controllers.auth import checkadmin
from db import session
from models import SLOModel, AssessmentModel, AssignedSLOModel
from marshal_base_fields import slo_fields, performance_indicator_fields, class_fields


slo_detailed_fields = {
    'performance_indicators': fields.List(fields.Nested(performance_indicator_fields)),
    'courses': fields.List(fields.Nested({'crn': fields.String(attribute='course.crn')}))
}

def perfList(performance_indicator):
  if 'performance_indicator_id' not in performance_indicator or 'performance_indicator_description' not in performance_indicator:
    raise ValueError("All perfcormance indicators must contain a performance_indicator_id and a performance_indicator_description.")

  return performance_indicator

parser = reqparse.RequestParser()
parser.add_argument('slo_description', type=str, required = True, help='SLO description field is required.')
parser.add_argument('performance_indicators', type=perfList, required = True, help='Valid performance indicators are required.', action='append')


class SLO(Resource):
    @jwt_required()
    @marshal_with({**slo_fields, **slo_detailed_fields})
    def get(self, slo_id):
        return session.query(SLOModel).filter(SLOModel.slo_id == slo_id).first()

    def put(self,slo_id):
        args = parser.parse_args()
        
        slo = session.query(SLOModel).filter(SLOModel.slo_id == slo_id).first()
        if not slo: abort(404, message="SLO doesn't exist") 

        slo.slo_description = args['slo_description']

        for performance_indicator in args['performance_indicators']:
            for db_perfindicator in slo.performance_indicators:
                if (db_perfindicator.performance_indicator_id == performance_indicator['performance_indicator_id']):
                    db_perfindicator.performance_indicator_description = performance_indicator['performance_indicator_description']

        session.commit()
        return slo


    def delete(self,slo_id):
        assigned_slo = session.query(AssignedSLOModel).filter(AssignedSLOModel.slo_id == slo_id).first()
        assessment = session.query(AssessmentModel).filter(AssessmentModel.slo_id == slo_id).first()
        if assigned_slo:
            if assessment:
                 abort(404, message="SLO is assigned to a course and has assessments using this SLO.")
            else:
                session.delete(slo)
                session.commit()
                return {}, 204 # Delete successful, so return empty 204 successful response


class SLOList(Resource):
    @jwt_required()
    @marshal_with({**slo_fields})
    def get(self):
        return session.query(SLOModel).all()
        