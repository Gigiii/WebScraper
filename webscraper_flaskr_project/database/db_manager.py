from sqlalchemy import create_engine, MetaData, Table, Column, String, Integer
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session
import os

#Create the database and the engine

db_url = f'sqlite:///WebScraper.db'
engine = create_engine(db_url, echo=True)

#Create a session factory and bind to the engine
session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

#Base class for models
Base = declarative_base()
Base.query = session.query_property()

#Model for countries table
class Countries(Base):

    __tablename__ = 'countries'
    #country name will be the primary key of the table
    name = Column(String, primary_key=True)

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return self.name

#Model for keywords table
class Keywords(Base):

    __tablename__ = 'keywords'
    #Keyword will be the primary key of the table
    keyword = Column(String, primary_key=True)
    #We will keep track of the count of indexes
    count = Column(Integer)
    
    def __init__(self, keyword=None, count=None):
        self.keyword = keyword
        self.count = count

    def __repr__(self):
        return f"{self.keyword}:{self.count}"
