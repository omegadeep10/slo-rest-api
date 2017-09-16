from flask_jwt import jwt_required, current_identity
from flask_restful import Resource
from controllers.auth import checkadmin
from db import session
from models import User

class HelloWorld(Resource):
    def get(self):
        data = session.query(User).first()
        return {
          'first_user': data.username
        }


class AdminProtected(Resource):
    @jwt_required()
    @checkadmin
    def get(self):
      return { 'congrats': current_identity['username'] }