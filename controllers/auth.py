from db import session
from models import User
from flask_jwt import JWT, jwt_required, current_identity
from flask_restful import abort
from functools import wraps

#temporary in-memory user database. In the real app, this would be replaced with a database call
users_data = [
  {
    "id": 1,
    "username": "user1",
    "password": "test1234",
    "is_admin": True
  },
  {
    "id": 2,
    "username": "user2",
    "password": "test1234",
    "is_admin": False
  }
]

#User object since flask-jwt requires one with an id param
class MyUser(object):
    def __init__(self, id, username):
        self.id = id
        self.username = username

    def __str__(self):
        return "User(id='%s')" % self.id


def authenticate(username, password):
  for user in users_data:
    if user['username'] == username and user['password'] == password:
      return MyUser(user["id"], user['username'])

def identity(payload):
  user_id = payload['identity']
  for user in users_data:
    if (user['id'] == user_id):
      return user

def checkadmin(func):
  @wraps(func)
  def wrapper(*args, **kwargs):
    if current_identity['is_admin']:
      return func(*args, **kwargs)
    return abort(401)
  return wrapper