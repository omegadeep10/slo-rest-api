from db import session
from models import User
from flask_jwt import JWT, jwt_required, current_identity
from flask_restful import abort
from functools import wraps
import sys


def authenticate(email, password):
  return session.query(User).filter(User.email == email, User.password == password).one_or_none()

def identity(payload):
  user_id = payload['identity']
  return session.query(User).filter(User.id == user_id).one_or_none()

def checkadmin(func):
  @wraps(func)
  def wrapper(*args, **kwargs):
    if current_identity.userType == "1":
      return func(*args, **kwargs)
    return abort(401)
  return wrapper