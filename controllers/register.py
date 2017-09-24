from flask_jwt import jwt_required, current_identity
from flask_restful import Resource
from controllers.auth import checkadmin
from db import session
from models import User
import sys

class Register(Resource):
  def post(self):
    me = User(email='',fname='',lname='',password='',userType='')
    if (email==''| fname == ''| lname == ''| password == ''| userType == ''):
      return {'You have a blank field.'}
    else:
      db.session.add(me)
      db.session.commit()
      return {'You are registered!'}
    #return {'register'}