from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class SLOModel(Base):
  __tablename__ = 'SLO'

  slo_id = Column(String(9),primary_key = True)
  slo_description = Column(String(255))

  def __str__(self):
    return "SLO object: (slo_id='%s')" % self.slo_id

  def __init__(self,slo_id,slo_description):
    self.slo_id = slo_id
    self.slo_description = slo_description