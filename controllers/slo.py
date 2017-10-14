from flask_jwt import jwt_required, current_identity
from flask_restful import Resource, reqparse, marshal_with, fields, abort
from controllers.auth import checkadmin
from db import session
from models import SLOModel
from marshal_base_fields import slo_fields, performance_indicator_fields


slo_detailed_fields = {
    'performance_indicators': fields.List(fields.Nested(performance_indicator_fields))
}

class SLO(Resource):
    @jwt_required()
    @marshal_with({**slo_fields, **slo_detailed_fields})
    def get(self, slo_id):
        return session.query(SLOModel).filter(SLOModel.slo_id == slo_id).first()
        