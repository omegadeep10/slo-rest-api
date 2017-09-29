from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class UserModel(Base):
    __tablename__ = 'Faculty'

    id = Column(Integer, primary_key=True)
    faculty_id = Column(String(9), unique=True, nullable=False)
    email = Column(String(255), nullable=False)
    first_name = Column(String(255))
    last_name = Column(String(255))
    password = Column(String(255), nullable=False)
    user_type = Column(String(1), nullable=False) # '0' = Regular User, '1' = Admin. Only two roles defined so far
    
    def __str__(self):
        return "User object: (id='%s')" % self.id
      
    def __init__(self, faculty_id, email, first_name, last_name, password, user_type):
        self.faculty_id = faculty_id
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.user_type = user_type