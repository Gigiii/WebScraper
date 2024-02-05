from crochet import setup, wait_for
setup() # Crochet Setup for handling the spider
import os
from flask import render_template, redirect, request, Blueprint
from .database.database_functions import *
from .generate_report import *

app_pages = Blueprint('app_pages', __name__, template_folder='templates')

# Main route responsible for rendering the showKeywords template
# alongside countries and keywords from the database
@app_pages.route('/')
def viewCountryKeywords():
    return render_template('showKeywords.html', countries=viewCountries(db),
                           country=request.args.get('country'), keywords=viewKeywords(db))

# Runs when the user selects a country to scrape from the main route.
# Calls runSpider() with the correct spider, generates a report,
# and then redirects the user to the homepage
@app_pages.route('/get', methods=['POST'])
def getKeywords():
    """
    Handles the '/get' route when the user selects a country to scrape.

    Returns:
        redirect: Redirects the user to the homepage with the selected country.
    """
    runSpider(f"{request.form['country']}_news")  # Run spider for the selected country
    generateReport(request.form['country'])  # Generate a report
    return redirect(f'/?country={request.form["country"]}')

# Run a specific spider
@app_pages.route('/run-spider/<spider>')
def runSpider(spider):
    """
    Runs a specific spider.

    Args:
        spider (str): Name of the spider to run.

    Returns:
        None
    """
    # Purge keywords from the last query
    purgeKeywords(db)
    # Crawl and wait for it to finish
    wait_for(os.system(f'scrapy crawl {spider}'))