from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from datetime import timedelta

app = Flask(__name__)
CORS(app)
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
from controllers.register import Register
from controllers.user import User
from controllers.assessment import Assessment, AssessmentList
from controllers.course import Course, CourseList
from controllers.student import Student

# NOTE: To obtain auth token, use the /auth endpoint, passing in a JSON object with email and password fields.
#       This endpoint is not shown here since it's automatically setup by flask_jwt.

api.add_resource(Register, '/register')      #<base_url>/register
api.add_resource(User,'/users')             #<base_url>/users
api.add_resource(AssessmentList,'/assessments')  #<base_url>/assessments
api.add_resource(Assessment,'/assessment/<int:assessment_id>') #<base_url>/assessments/<assessment_id>
api.add_resource(CourseList,'/courses')         #<base_url>/classes
api.add_resource(Course,'/course/<string:crn>')  #<base_url>/classes/<CRN>
api.add_resource(Student,'/student')             #<base_url>/student

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True) # runs on an internal ip at port 3000 that codeanywhere's linux box automatically maps to external IP
                                                   # To get the external IP, right click on 'python-backend' and click info to view relevant details