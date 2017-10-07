from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class AssignedSLOModel(Base):
    __tablename__ = 'AssignedSLO'

    slo_id = Column(String(3), primary_key=True)
    CRN = Column(String(5), primary_key=True)
    
    def __str__(self):
        return "AssignedSLO object: (slo_id='%s')" % self.slo_id
      
    def __init__(self,slo_id, CRN):
      self.slo_id = slo_id
      self.CRN = CRN