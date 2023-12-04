from sqlalchemy import Column, Integer, String
from db import Base

class Keywords(Base):
    __tablename__ = 'keywords'
    keyword = Column(String, primary_key=True)
    count = Column(Integer)
    

