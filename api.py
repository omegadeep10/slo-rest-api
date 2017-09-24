from flask import Flask
from flask_restful import Resource, Api, abort

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tacos_21'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://db_team:fudge1960@45.55.81.224/slo?charset=utf8&use_unicode=0'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # we don't use track mods, this gets rid of an error in the console

api = Api(app)

from flask_jwt import JWT, jwt_required, current_identity
from controllers.auth import authenticate, identity, checkadmin
jwt = JWT(app, authenticate, identity)


from controllers.hello_world import HelloWorld, AdminProtected
from controllers.register import Register
from controllers.users import Users
from controllers.assessments import Assessments
from controllers.classes import Classes
api.add_resource(HelloWorld, '/')           #<base_url>/
api.add_resource(AdminProtected, '/admin')  #<base_url/admin
api.add_resource(Register, '/register')     #<base_url>/register
api.add_resource(Users,'/users')            #<base_url>/users
api.add_resource(Assessments,'/assessments') #<base_url>/assessments
api.add_resource(Classes,'/classes')        #<base_url>/classes

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)