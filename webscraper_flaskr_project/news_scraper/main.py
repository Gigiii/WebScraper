from crochet import setup, wait_for
#Crochet Setup
setup()
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from webscraper_flaskr_project.database.db_manager import session
from webscraper_flaskr_project.database.queries import *
from webscraper_flaskr_project.news_scraper.news_scraper.spiders.news_spiders import *
from flask import Flask, render_template, redirect, request
from flask_bootstrap import Bootstrap

def create_app(test_config=None):

    # create and configure the app  
    app = Flask(__name__, instance_relative_config=True)
    Bootstrap(app)
    app.config.from_mapping(
        SECRET_KEY='devKeyForTestingPurposes123592',
        DATABASE=os.path.join(app.instance_path, 'WebScraper.db'),
    )
    
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        session.remove()

    
    @app.route('/')
    def viewCountryKeywords():
        return render_template('showKeywords.html', countries = viewCountries(), country=request.args.get('country'),
                               keywords = viewKeywords())

    @app.route('/get', methods=['POST'])
    def get_keywords():
        run_spider(f"{request.form['country']}_news")
        return redirect(f'/?country={request.form["country"]}')

    @app.route('/run-spider/<spider>')
    def run_spider(spider):
        print(f"Current spider = {spider}")
        purgeKeywords()
        wait_for(os.system(f'scrapy crawl {spider}'))
        return f'Spider: {spider} finished scraping'
    
    return app