from flask_jwt import jwt_required, current_identity
from flask_restful import Resource, reqparse, marshal_with, fields, abort
from controllers.auth import checkadmin
from db import session
from models import SLOModel, PerfIndicatorModel

class SLO(Resource):
    @jwt_required()
    def get(self):
        return {'data'}