from sqlalchemy import Column, Integer,UniqueConstraint,String
from .base import *


class Cach(Base):
    __tablename__ = 'Cach'
    id = Column(Integer, primary_key=True)
    chatid = Column(Integer)
    key = Column(String)
    value = Column(String)
    


    # __table_args__ = (
    #     UniqueConstraint('chatid', 'key', name='uix_chatid_key'),
    # )