from sqlalchemy import Column, Integer, String, DateTime
from .base import *

class Step(Base):
    __tablename__ = 'Step'
    id = Column(Integer, primary_key=True)
    chatid = Column(Integer)
    step = Column(String)
