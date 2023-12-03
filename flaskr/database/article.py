from sqlalchemy import Column, Integer, String, Date
from db import Base

class Article(Base):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    country = Column(String)
    publication_name = Column(String)
    headlines = Column(String)
    retrieval_date = Column(Date)

    

