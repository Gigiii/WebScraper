from crochet import setup, wait_for
#Crochet Setup for handling spider
setup()
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from news_scraper import *
from flask import Flask, render_template, redirect, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import String, Integer, Column, desc
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.lib.colors import PCMYKColor
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY
import datetime as dt

def create_app(test_config=None):
    #Create Base and db to connect with SQLAlchemy through Flask-SQLAlchemy
    class Base(DeclarativeBase):
        pass
    db = SQLAlchemy(model_class=Base)

    # create and configure the app  
    app = Flask(__name__, instance_relative_config=True)
    Bootstrap(app)
    app.config.from_mapping(
        SECRET_KEY='devKeyForTestingPurposes123592',
        SQLALCHEMY_DATABASE_URI = 'sqlite:///../news_scraper/WebScraper.db'
    )
    db.init_app(app)

    #Create the Models to be initiated into the database
    #Model for countries table
    class Countries(db.Model):
        __tablename__ = "countries"
        #country name will be the primary key of the table
        name = Column(String, primary_key=True)

        def __init__(self, name=None):
            self.name = name

        def __repr__(self):
            return self.name

    #Model for keywords table
    class Keywords(db.Model):
        __tablename__ = 'keywords'
        #Keyword will be the primary key of the table
        keyword = Column(String, primary_key=True)
        #We will keep track of the count of indexes
        count = Column(Integer)
        
        def __init__(self, keyword=None, count=None):
            self.keyword = keyword
            self.count = count

        def __repr__(self):
            return f"{self.keyword}:{self.count}"

    #Ensureed the models are created in the database  
    with app.app_context():
        db.create_all()
    
    #Create the functions to control the database
    #Delete all entries in the keywords table
    def purgeKeywords(db):

        db.session.query(Keywords).delete()
        db.session.commit()

    #Delete past keywords from last time the program was ran
    with app.app_context():
        purgeKeywords(db)
    
    #View 15 keywords, sorted by count descendingly
    def viewKeywords(db):
        keywords = (Keywords.query.order_by(desc(Keywords.count)).limit(15)).all()
        return keywords
    
    #View all the countries supported
    def viewCountries(db):
        countries = Countries.query.all()
        return countries

    #Turn off session
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    #Main route, responsible for rendering the showKeywords template alongside the countries and keywords from database
    @app.route('/')
    def viewCountryKeywords():
        return render_template('showKeywords.html', countries = viewCountries(db), country=request.args.get('country'),
                               keywords = viewKeywords(db))

    #Runs when the user selects a country to scrape from the main route.
    #call runSpider() with the correct spider, afterwards generate report, and then redirect user to homepage
    @app.route('/get', methods=['POST'])
    def getKeywords():
        runSpider(f"{request.form['country']}_news")
        generateReport(request.form['country'])
        return redirect(f'/?country={request.form["country"]}')

    #Run a select spider
    @app.route('/run-spider/<spider>')
    def runSpider(spider):
        #Purge keywords from last query
        purgeKeywords(db)
        #Crawl and wait for it to finish
        wait_for(os.system(f'scrapy crawl {spider}'))
    
    #Generates the report
    @app.route('/report-generator')
    def generateReport(country):

        # Get the default style sheet
        styles = getSampleStyleSheet()

        # Create a SimpleDocTemplate
        doc = SimpleDocTemplate(f"../report_{country}_{dt.date.today()}.pdf", pagesize=letter)

        # Container for the 'Flowable' objects
        elements = []

        #Create the style for paragraphs with spacing and justify
        paragraph_style = ParagraphStyle(
            'ParagraphWithSpace',
            parent=styles['Normal'],
            spaceAfter=12,
            spaceBefore=6,
            alignment=TA_JUSTIFY,
        )

        #Create the headline, date, and paragraph 1 and add it into the elements
        headline = Paragraph(f"Report scraping {country}", styles['Heading1'])
        date = Paragraph(f"Today's date: {dt.date.today()}", styles['Heading2'])
        paragraph_1_text = """
                            Welcome to our web application, a powerful tool 
                            that scrapes news websites to bring you the most 
                            relevant and trending information. Our application 
                            dives deep into the vast ocean of online news content 
                            and extracts the most used keywords to give you a 
                            clear picture of what's happening around the world.

                            The data table you see below is the result of our 
                            sophisticated analysis. It shows the most frequently 
                            used keywords across different websites, providing a 
                            unique insight into the topics that are currently 
                            dominating the news landscape. Each row in the table 
                            represents a keyword, while the third column provide 
                            detailed information about the keyword's frequency, 
                            the news sites where it's most commonly found, and 
                            its overall popularity.

                            Explore the table, discover the trends and dive 
                            into the stories that matter most to you. 
                            Happy exploring!
                               """
        paragraph1 = Paragraph(paragraph_1_text, paragraph_style)
        elements.append(headline)
        elements.append(date)
        elements.append(paragraph1)

        #Get the 15 top keywords from the database
        keywords = viewKeywords(db)

        # Generate the data list necessary for the table
        data = [
            ['index', 'Keyword', 'Count'],
        ]
        indexed_keywords = [[i+1, item.keyword, item.count] for i, item in enumerate(keywords)]
        filled_data = data+indexed_keywords

        # Create a Table with the data
        t = Table(filled_data)

        # Add grid to table
        table_style = TableStyle([
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ])
        t.setStyle(table_style)

        # Add table to elements
        elements.append(t)

        #Create text for paragraph 2 and add it into the elements
        paragraph_2_text = """
                Welcome to the histogram view of our data table. This
                visual representation shows the top 15 most used keywords
                from different news sites, ranked from the highest to the
                 lowest number of hits.
                 """
        
        paragraph2 = Paragraph(paragraph_2_text, paragraph_style)
        elements.append(paragraph2)

        #Create the bar data necessary for generation
        bar_data = [(item.keyword , item.count) for i, item in enumerate(keywords)]
        keywords, counts = zip(*bar_data)
    
        # Create a Drawing object that will contain the chart
        drawing = Drawing(400, 200)

        # Create the bar chart
        bc = VerticalBarChart()
        bc.x = 50
        bc.y = 50
        bc.height = 125
        bc.width = 300
        bc.data = [counts]
        bc.strokeColor = PCMYKColor(0, 0, 0, 0)
        bc.valueAxis.valueMin = 0
        bc.valueAxis.valueMax = counts[0]
        bc.valueAxis.valueStep = 5
        bc.categoryAxis.labels.boxAnchor = 'ne'
        bc.categoryAxis.labels.dx = 8
        bc.categoryAxis.labels.dy = -2
        bc.categoryAxis.labels.angle = 30
        bc.categoryAxis.categoryNames = keywords

        # Add the bar chart to the drawing
        drawing.add(bc)

        # Add the drawing to the elements
        elements.append(drawing)

        #Create text for paragraph 3 and add it into the elements
        paragraph_3_text = """
                        This concludes our brief analysis for our programming
                         languages assignment. It's important to realise that
                         the keywords presented here are based on a limited 
                         amount of information. The reality we perceive through 
                         the Internet is often a condensed version of the real 
                         world, and this application is no exception. While our 
                         tool provides valuable insights, users should be aware 
                         that it represents only a fraction of the vast information 
                         landscape. Always remember to approach online information 
                         with a critical mind and an understanding of its inherent 
                         limitations. Thank you for using our application!
        """
        paragraph3 = Paragraph(paragraph_3_text, paragraph_style)
        elements.append(paragraph3)

        # Build the PDF
        doc.build(elements)
    

    return app