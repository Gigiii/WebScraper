import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from webscraper_flaskr_project.database.db_manager import session, Base, engine, Keywords, Countries
from sqlalchemy import desc

#Initiate the databse and the models
def init_db():
    Base.metadata.create_all(bind=engine)


#Delete all entries in the keywords table
def purgeKeywords():

    session.query(Keywords).delete()
    session.commit()

#View 15 keywords, sorted by count descendingly
def viewKeywords():

    keywords = session.query(Keywords).order_by(desc(Keywords.count)).limit(15).all()
    return keywords

#Insert the 4 countries supported
def insertCountries():

    america = Countries(name='American')
    uk = Countries(name='Britain')
    germany = Countries(name='Germany')
    singapore = Countries(name='Singapore')

    session.add_all([america, uk, germany, singapore])
    session.commit()

#View all the countries supported
def viewCountries():

    countries = session.query(Countries).all()
    return countries

# Commands for debugging purposes
# init_db()
# insertCountries()
# print(viewKeywords())
# print(viewCountries())
# purgeKeywords()