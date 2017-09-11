from flask_jwt import jwt_required, current_identity
from flask_restful import Resource
from controllers.auth import checkadmin

class HelloWorld(Resource):
    @jwt_required()
    def get(self):
        return { 'hello': current_identity['username'] }


class AdminProtected(Resource):
    @jwt_required()
    @checkadmin
    def get(self):
      return { 'congrats': current_identity['username'] }