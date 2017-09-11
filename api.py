from flask import Flask
from flask_restful import Resource, Api, abort
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tacos_21'
api = Api(app)

from flask_jwt import JWT, jwt_required, current_identity
from controllers.auth import authenticate, identity, checkadmin
jwt = JWT(app, authenticate, identity)


from controllers.hello_world import HelloWorld, AdminProtected
api.add_resource(HelloWorld, '/')           #<base_url>/
api.add_resource(AdminProtected, '/admin')  #<base_url/admin

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)