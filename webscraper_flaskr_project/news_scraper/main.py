from news_scraper import *
from flask import Flask
from flask_bootstrap import Bootstrap
from .database.database_creation import db
from .database.database_models import *
from .database.database_functions import *
from .generate_report import *
from .app_routes import *

def create_app(test_config=None):
    """
    Creates and configures the Flask app.

    Args:
        test_config (dict, optional): Configuration for testing (default: None).

    Returns:
        Flask: Initialized Flask app.
    """

    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.register_blueprint(app_pages) #register the routes of the app through a blueprint
    Bootstrap(app)  # Initialize Bootstrap for styling
    app.config.from_mapping(
        SECRET_KEY='devKeyForTestingPurposes123592',  # Set a secret key for session management
        SQLALCHEMY_DATABASE_URI='sqlite:///../news_scraper/WebScraper.db',  # SQLite database URI
    )
    db.init_app(app)  # Initialize SQLAlchemy with the app

    # Ensure the models are created in the database
    with app.app_context():
        db.create_all()

    # Delete past keywords from the last time the program was run
    with app.app_context():
        purgeKeywords(db)

    # Turn off session
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    return app