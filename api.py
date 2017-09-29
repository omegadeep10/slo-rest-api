from flask import Flask
from flask_restful import Api
from datetime import timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tacos_21' # used for signing tokens
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://db_team:fudge1960@45.55.81.224/slo?charset=utf8&use_unicode=0'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # we don't use track mods, this gets rid of an error in the console
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=3600) # default to JWT expiration of one hour
app.config['JWT_AUTH_USERNAME_KEY'] = 'email' # we use email, not the default 'username' field that flask_JWT expects

api = Api(app)

#initialize flask_JWT
from flask_jwt import JWT, jwt_required, current_identity
from controllers.auth import authenticate, identity, checkadmin
jwt = JWT(app, authenticate, identity)


# Importing various api resources
from controllers.hello_world import HelloWorld, AdminProtected
from controllers.register import Register
from controllers.users import User
from controllers.assessments import Assessments, AssessmentsList
from controllers.classes import Classes, ClassesList

# NOTE: To obtain auth token, use the /auth endpoint, passing in a JSON object with email and password fields.
#       This endpoint is not shown here since it's automatically setup by flask_jwt.

api.add_resource(HelloWorld, '/')            #<base_url>/
api.add_resource(AdminProtected, '/admin')   #<base_url/admin
api.add_resource(Register, '/register')      #<base_url>/register
api.add_resource(User,'/users')             #<base_url>/users
api.add_resource(AssessmentsList,'/assessments')  #<base_url>/assessments
api.add_resource(Assessments,'/assessments/<int:assessment_id>') #<base_url>/assessments/<assessment_id>
api.add_resource(ClassesList,'/classes')         #<base_url>/classes
api.add_resource(Classes,'/classes/<int:CRN>')  #<base_url>/classes/<CRN>

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True) # runs on an internal ip at port 3000 that codeanywhere's linux box automatically maps to external IP
                                                   # To get the external IP, right click on 'python-backend' and click info to view relevant details