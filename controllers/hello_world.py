from flask_jwt import jwt_required, current_identity
from flask_restful import Resource
from controllers.auth import checkadmin
from db import session
from models import User
import sys

class HelloWorld(Resource):
    @jwt_required()
    def get(self):
        print(type(current_identity.email), sys.stdout)
        return { 'congrats': current_identity.email.decode('utf-8') }


class AdminProtected(Resource):
    @jwt_required()
    @checkadmin
    def get(self):
      return { 'congrats': current_identity['email'] }