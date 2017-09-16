from db import session
from models import User
from flask_jwt import JWT, jwt_required, current_identity
from flask_restful import abort
from functools import wraps
import sys


def authenticate(username, password):
  return session.query(User).filter(User.username == username, User.password == password).one_or_none()

def identity(payload):
  user_id = payload['identity']
  print(user_id, sys.stdout)
  return session.query(User).filter(User.id == user_id).first()

def checkadmin(func):
  @wraps(func)
  def wrapper(*args, **kwargs):
    if current_identity.is_admin == "True":
      return func(*args, **kwargs)
    return abort(401)
  return wrapper