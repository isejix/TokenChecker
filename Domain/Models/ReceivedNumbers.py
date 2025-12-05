from sqlalchemy import Column, Integer, String,Enum
from .base import *
import enum


class SessionStatus(enum.Enum):
    
    Accepted = "Accepted"
    Pending = "Pending"
    Ban = "Ban"
    Other = "Other"
    
class ReciveNumber(Base):
    __tablename__ = 'ReciveNumber'
    id = Column(Integer, primary_key=True)
    number = Column(String)
    link = Column(String)
    path = Column(String)
    status = Column(Enum(SessionStatus), default=SessionStatus.Accepted)