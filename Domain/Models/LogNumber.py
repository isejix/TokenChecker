from sqlalchemy import Column, Integer, String
from .base import *


    
class LogNUmber(Base):
    __tablename__ = 'LogNUmber'
    id = Column(Integer, primary_key=True)
    number = Column(String)
    email = Column(String,nullable=True,default="-")
    code = Column(Integer)  
    name = Column(String)
    link = Column(String)  

    
    
    