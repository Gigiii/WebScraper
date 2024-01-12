from sqlalchemy import Column, Integer, String
from db_manager import Base

#Model for keywords table
class Keywords(Base):
    __tablename__ = 'keywords'
    #Keyword will be the primary key of the table
    keyword = Column(String, primary_key=True)
    #We will keep track of the count of indexes
    count = Column(Integer)
    
