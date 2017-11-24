from flask_jwt import jwt_required, current_identity
from flask_restful import Resource, fields, marshal_with, reqparse, abort
from controllers.auth import checkadmin
from models import FacultyModel
from db import session
from marshal_base_fields import faculty_fields

faculty_extra_fields = {
	'id': fields.Integer,
	'user_type': fields.String,
    'total_courses': fields.Integer(attribute=lambda x: len(x.courses))
}

class AccountList(Resource):
    @jwt_required()
    @checkadmin
    @marshal_with({**faculty_fields, **faculty_extra_fields})
    def get(self):
        return session.query(FacultyModel).all()


parser = reqparse.RequestParser()
parser.add_argument('email', type=str, required = True, help='Email field is required.')
parser.add_argument('faculty_id', type=str, required = True, help='Faculty ID field is required.')
parser.add_argument('first_name', type=str, required = True, help='First Name field is required.')
parser.add_argument('last_name', type=str, required = True, help='Last Name field is required.')
parser.add_argument('user_type', type=str, required = True, help='User type is required.')

class Account(Resource):
    @jwt_required()
    @checkadmin
    @marshal_with({**faculty_fields, **faculty_extra_fields})
    def get(self, account_id):
        account = session.query(FacultyModel).filter(FacultyModel.id == account_id).first()
        if not account: abort(404, message="Account with the id {} was not found".format(account_id))

        return account
    
    @jwt_required()
    @checkadmin
    @marshal_with({**faculty_fields, **faculty_extra_fields})
    def put(self, account_id):
        account = session.query(FacultyModel).filter(FacultyModel.id == account_id).first()
        if not account: abort(404, message="Account with the id {} was not found".format(account_id))

        args = parser.parse_args()
        if args['user_type'] != '1' and args['user_type'] != '0':
            abort(422, message="user_type must be 1 or 0")
        
        account.email = args['email']
        account.faculty_id = args['faculty_id']
        account.first_name = args['first_name']
        account.last_name = args['last_name']
        account.user_type = args['user_type']

        session.commit()
        return account

    def delete(self, account_id):
        account = session.query(FacultyModel).filter(FacultyModel.id == account_id).first()
        if not account: abort(404, message="Account with the id {} was not found".format(account_id))

        session.delete(account)
        session.commit()

        return {}, 204


resetParser = reqparse.RequestParser()
resetParser.add_argument('password', type=str, required = True, help='Password field is required.')

class ResetPassword(Resource):
    @jwt_required()
    @checkadmin
    @marshal_with({**faculty_fields, **faculty_extra_fields})
    def post(self, account_id):
        account = session.query(FacultyModel).filter(FacultyModel.id == account_id).first()
        if not account: abort(404, message="Account with the id {} was not found".format(account_id))

        args = resetParser.parse_args()
        if not args['password'] or len(args['password']) < 8:
            abort(422, message="password is required and must be a minimum of 8 characters")
        
        account.password = args['password']
        session.commit()

        return account