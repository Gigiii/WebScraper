from sqlalchemy import desc
from .database_creation import db
from .database_models import *

# Functions to control the database

def purgeKeywords(db):
    """
    Deletes all entries in the keywords table.

    Args:
        db: SQLAlchemy database session.

    Returns:
        None
    """
    db.session.query(Keywords).delete()
    db.session.commit()
    
def viewKeywords(db):
    """
    Retrieves 15 keywords sorted by count in descending order.

    Args:
        db: SQLAlchemy database session.

    Returns:
        list: List of Keywords objects.
    """
    keywords = (Keywords.query.order_by(desc(Keywords.count)).limit(15)).all()
    return keywords

def viewCountries(db):
    """
    Retrieves all countries supported.

    Args:
        db: SQLAlchemy database session.

    Returns:
        list: List of Countries objects.
    """
    countries = Countries.query.all()
    return countries