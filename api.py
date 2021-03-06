from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from db import session
from datetime import timedelta

app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = 'tacos_21' # used for signing tokens
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://db_team:fudge1960@45.55.81.224/slo?charset=utf8&use_unicode=0'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # we don't use track mods, this gets rid of an error in the console
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=3600) # default to JWT expiration of one hour
app.config['JWT_AUTH_USERNAME_KEY'] = 'email' # we use email, not the default 'username' field that flask_JWT expects
app.config['ERROR_404_HELP'] = False

api = Api(app)
CORS(app)

@app.teardown_appcontext
def close_session(exception=None):
    session.remove()

#initialize flask_JWT
from flask_jwt import JWT, jwt_required, current_identity
from controllers.auth import authenticate, identity, checkadmin
jwt = JWT(app, authenticate, identity)


# Importing various api resources
from controllers.register import Register
from controllers.user import User
from controllers.assessment import Assessment, AssessmentList
from controllers.course import Course, CourseList
from controllers.student import Student, BatchStudent
from controllers.slo import SLO, SLOList, SLOArchive
from controllers.progress import Progress
from controllers.report import CourseReports, SLOReports
from controllers.data import CourseDataList, SLODataList
from controllers.account import AccountList, Account, ResetPassword

# NOTE: To obtain auth token, use the /auth endpoint, passing in a JSON object with email and password fields.
#       This endpoint is not shown here since it's automatically setup by flask_jwt.

# /register => POST
api.add_resource(Register, '/register')
# /users => GET
api.add_resource(User,'/users')

# /assessments/<crn> => GET, POST
api.add_resource(AssessmentList,'/assessments/<string:crn>')
# /assessment/<assessment_id> => GET, PUT, DELETE
api.add_resource(Assessment,'/assessment/<int:assessment_id>')

# /courses => GET, POST
api.add_resource(CourseList,'/courses')
# /course/<crn> => GET, PUT, DELETE
api.add_resource(Course,'/course/<string:crn>')

# /student/<student_id> => GET, POST
api.add_resource(Student,'/student/<string:student_id>')
# /student/batch => POST
api.add_resource(BatchStudent, '/students/batch/<string:crn>')

# /slo/<slo_id> => GET
api.add_resource(SLO, '/slo/<string:slo_id>')
# /slos => GET
api.add_resource(SLOList, '/slos')

# /slo/<slo_id>/archive
api.add_resource(SLOArchive, '/slo/<string:slo_id>/archive')

# /progress => GET
api.add_resource(Progress, '/progress')

# /report/courses => GET
api.add_resource(CourseReports,'/report/courses')
# /report/slos => GET
api.add_resource(SLOReports, '/report/slos')

# /data/course/<crn> => GET
api.add_resource(CourseDataList, '/data/course/<string:crn>')
# /data/slo/<slo_id> => GET
api.add_resource(SLODataList, '/data/slo/<string:slo_id>')

# /accounts => GET
api.add_resource(AccountList, '/accounts')
# /account/<account_id> => GET, PUT, DELETE
api.add_resource(Account, '/account/<int:account_id>')

# /resetpassword/<account_id> => POST
api.add_resource(ResetPassword, '/resetpassword/<int:account_id>')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)