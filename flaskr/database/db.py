from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#Create the database and the engine
db_url = 'sqlite:///WebScraper.db'
engine = create_engine(db_url, echo=True)

#Create a session factory and bind to the engine
sessionBinder = sessionmaker(bind=engine)
session = sessionBinder()

#Base class for models
Base = declarative_base()