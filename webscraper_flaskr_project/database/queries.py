from models.keywords import Keywords
from sqlalchemy import desc
from sqlalchemy.sql import text
from db_manager import session, Base, engine

#Inserts a singular keyword and updates the count if it already exists in the database
def insertKeyword(keyword, count):
    keyword_model = Keywords()
    keyword_model.keyword = keyword
    keyword_model.count = count
    existing_entry = session.query(Keywords).filter(Keywords.keyword == keyword).first()
    if existing_entry:
        existing_entry.count += keyword_model.count
    else:
        session.add(keyword_model)
    return session.commit()

#Delete all entries in the keywords table
def purgeKeywords():
    session.query(Keywords).delete()
    session.commit()

def viewKeywords():
    keywords = session.query(Keywords).order_by(desc(Keywords.count)).limit(10).all()

    for keyword in keywords:
        print(keyword.keyword, keyword.count)


viewKeywords()
purgeKeywords()