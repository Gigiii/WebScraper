from sqlalchemy.orm import DeclarativeBase
from flask_sqlalchemy import SQLAlchemy


# Create Base and db to connect with SQLAlchemy through Flask-SQLAlchemy
class Base(DeclarativeBase):
    pass
db = SQLAlchemy(model_class=Base)