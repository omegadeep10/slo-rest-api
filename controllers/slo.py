from flask_jwt import jwt_required, current_identity
from flask_restful import Resource, reqparse, marshal_with, fields, abort
from controllers.auth import checkadmin
from db import session
from models import SLOModel

performance_indicator_fields = {
    'performance_indicator_id': fields.String,
    'performance_indicator_description': fields.String,
    'unsatisfactory_description': fields.String,
    'developing_description': fields.String,
    'satisfactory_description': fields.String,
    'exemplary_description': fields.String
}

slo_fields = {
	'slo_id': fields.String,
	'slo_description': fields.String,
    'performance_indicators': fields.List(fields.Nested(performance_indicator_fields))
}

class SLO(Resource):
    @jwt_required()
    @marshal_with(slo_fields)
    def get(self,slo_id):
        return session.query(SLOModel).filter(SLOModel.slo_id == slo_id).first()
        