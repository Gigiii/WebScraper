from sqlalchemy import String, Integer, Column
from .database_creation import db

# Create the Models to be initiated into the database
# Model for countries table
class Countries(db.Model):
    """
    Represents the Countries table in the database.

    Attributes:
        name (str): Primary key for the table (country name).

    Methods:
        __init__(self, name=None): Initializes a Countries instance.
        __repr__(self): Returns a string representation of the Countries object.
    """
    __tablename__ = "countries"
    name = Column(String, primary_key=True)

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return self.name

# Model for keywords table
class Keywords(db.Model):
    """
    Represents the Keywords table in the database.

    Attributes:
        keyword (str): Primary key for the table.
        count (int): Keeps track of the count of indexes.

    Methods:
        __init__(self, keyword=None, count=None): Initializes a Keywords instance.
        __repr__(self): Returns a string representation of the Keywords object.
    """
    __tablename__ = 'keywords'
    keyword = Column(String, primary_key=True)
    count = Column(Integer)

    def __init__(self, keyword=None, count=None):
        self.keyword = keyword
        self.count = count

    def __repr__(self):
        return f"{self.keyword}:{self.count}"
