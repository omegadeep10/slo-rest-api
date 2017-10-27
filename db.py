from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

db_url = 'mysql+pymysql://db_team:fudge1960@45.55.81.224/slo?charset=utf8&use_unicode=0'

Session = sessionmaker(autocommit=False, autoflush=False, bind=create_engine(db_url, convert_unicode=True, pool_size=100, pool_recycle=3600))
session = scoped_session(Session)