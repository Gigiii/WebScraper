from crochet import setup, wait_for
#Crochet Setup
setup()
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from webscraper_flaskr_project.database.db_manager import session
from webscraper_flaskr_project.database.queries import *
from webscraper_flaskr_project.news_scraper.news_scraper.spiders.news_spiders import *
from flask import Flask, render_template, redirect, request, send_file
from flask_bootstrap import Bootstrap
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
        generate_report(request.form['country'])
        return redirect(f'/?country={request.form["country"]}')

    @app.route('/run-spider/<spider>')
    def run_spider(spider):
        print(f"Current spider = {spider}")
        purgeKeywords()
        wait_for(os.system(f'scrapy crawl {spider}'))
        return f'Spider: {spider} finished scraping'
    
    @app.route('/report-generator')
    def generate_report(country):

        # Get the default style sheet
        styles = getSampleStyleSheet()

        # Create a SimpleDocTemplate
        doc = SimpleDocTemplate("../report.pdf", pagesize=letter)
        # Container for the 'Flowable' objects
        elements = []

        paragraph_style = ParagraphStyle(
            'ParagraphWithSpace',
            parent=styles['Normal'],
            spaceAfter=12,
            spaceBefore=6,
            alignment=TA_JUSTIFY,
        )

        headline = Paragraph(f"Report scraping {country}", styles['Heading1'])
        date = Paragraph(f"Today's date: {dt.date.today()}", styles['Heading2'])
        paragraph1_text = """
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
        paragraph1 = Paragraph(paragraph1_text, paragraph_style)
        elements.append(headline)
        elements.append(date)
        elements.append(paragraph1)

        keywords = viewKeywords()
        print(f"keywords: {keywords}")
        # Data in a form of list of lists
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

        paragraph2_text = """
                Welcome to the histogram view of our data table. This
                visual representation shows the top 15 most used keywords
                from different news sites, ranked from the highest to the
                 lowest number of hits.
                 """
        
        paragraph2 = Paragraph(paragraph2_text, paragraph_style)
        elements.append(paragraph2)

        bar_data = [(item.keyword , item.count) for i, item in enumerate(keywords)]
        keywords, counts = zip(*bar_data)
        print(f'seperated keywords = {keywords}')
        print(f'seperated counts = {counts}')
    
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

        paragraph3_text = """
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
                         limitations. Thank you for using our application!
        """
        paragraph3 = Paragraph(paragraph3_text, paragraph_style)
        elements.append(paragraph3)

        # Build the PDF
        doc.build(elements)
    

        
    return app