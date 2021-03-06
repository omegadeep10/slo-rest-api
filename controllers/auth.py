from db import session
from models import FacultyModel
from flask_jwt import JWT, jwt_required, current_identity
from flask_restful import abort
from functools import wraps
from flask import request
import sys

# The authentication handler used by flask_JWT. Takes an email and password
def authenticate(email, password):
  #Query the database and return the ONE user that has the matching email/password. If user doesn't exist, return None
  faculty = session.query(FacultyModel).filter(FacultyModel.email == email).one_or_none()
  if (faculty and faculty.check_password(password)):
    return faculty
  else:
    return None

# payload = JWT token sent by the user (as a header attribute)
# gets the ID stored within the token and returns the user object using the id to query the database
def identity(payload):
  user_id = payload['identity']
  return session.query(FacultyModel).filter(FacultyModel.id == user_id).one_or_none()


# wrapper function that checks that the currently logged in user is an admin. If not, aborts with a 401 status code
def checkadmin(func):
  @wraps(func)
  def wrapper(*args, **kwargs):
    if current_identity.user_type == "1": # One is the admin code
      return func(*args, **kwargs)
    return abort(401)
  return wrapper
