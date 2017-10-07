from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class PerfIndicatorModel(Base):
    __tablename__ = 'PerformanceIndicator'
    
    performance_indicator_id = Column(String(5),primary_key=True)
    slo_id = Column(String(3))
    performance_indicator_description = Column(String(255))
    unsatisfsctory_description = Column(String(500))
    developing_description = Column(String(500))
    satisfactory_description = Column(String(500))
    exempary_description = Column(String(500))

    def __str__(self):
      return "PerfIndicator object: (performance_indicator_id='%s')" % self.performance_indicator_id
    
    def __init__(self,performance_indicator_id,slo_id,performance_indicator_description,unsatisfactory_description,developing_description,satisfaction_description,exemplary_description):
      self.performance_indicator_id = performance_indicator_id
      self.slo_id = slo_id
      self.performance_indicator_description = performance_indicator_description
      self.unsatisfsctory_description = unsatisfactory_description
      self.developing_description = developing_description
      self.satisfactory_description = satisfaction_description
      self.exempary_description = exemplary_description
    