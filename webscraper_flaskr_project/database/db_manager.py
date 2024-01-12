from sqlalchemy import create_engine, MetaData, Table, Column, String, Integer
from sqlalchemy.orm import sessionmaker, declarative_base

#Create the database and the engine
db_url = 'sqlite:///WebScraper.db'
engine = create_engine(db_url, echo=True)

#Create a session factory and bind to the engine
sessionBinder = sessionmaker(bind=engine)
session = sessionBinder()

#Creates the metadata for the table and insert it into the database
metadata = MetaData()
keywords = Table(
    'keywords',
    metadata,
    Column('keyword', String, primary_key=True),
    Column('count', Integer),
)

metadata.create_all(engine)

#Base class for models
Base = declarative_base()
