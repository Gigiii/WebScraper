import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from webscraper_flaskr_project.database.db_manager import session, Base, engine, Keywords, Countries
from sqlalchemy import desc, insert
from sqlalchemy.sql import text

def init_db():
    Base.metadata.create_all(bind=engine)


#Delete all entries in the keywords table
def purgeKeywords():

    session.query(Keywords).delete()
    session.commit()

def viewKeywords():

    keywords = session.query(Keywords).order_by(desc(Keywords.count)).limit(10).all()
    return keywords

def insertCountries():

    america = Countries(name='American')
    uk = Countries(name='Uk')
    germany = Countries(name='German')
    singapore = Countries(name='Singapore')

    session.add_all([america, uk, germany, singapore])
    session.commit()

def viewCountries():
    countries = session.query(Countries).all()
    return countries

# init_db()
# insertCountries()
print(viewKeywords())
print(viewCountries())
# purgeKeywords()