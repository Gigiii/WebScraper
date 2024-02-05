from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.lib.colors import PCMYKColor
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY
import datetime as dt
from .database.database_functions import viewKeywords
from .database.database_creation import db

def generateReport(country):
    """
    Generates a report.

    Args:
        country (str): Country name for the report.

    Returns:
        None
    """
    # Get the default style sheet
    styles = getSampleStyleSheet()

    # Create a SimpleDocTemplate
    doc = SimpleDocTemplate(f"../report_{country}_{dt.date.today()}.pdf", pagesize=letter)

    # Container for the 'Flowable' objects
    elements = []

    # Create the style for paragraphs with spacing and justify
    paragraph_style = ParagraphStyle(
        'ParagraphWithSpace',
        parent=styles['Normal'],
        spaceAfter=12,
        spaceBefore=6,
        alignment=TA_JUSTIFY,
    )

    # Create the headline, date, and paragraph 1 and add them to the elements
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

    # Get the 15 top keywords from the database
    keywords = viewKeywords(db)

    # Generate the data list necessary for the table
    data = [
        ['index', 'Keyword', 'Count'],
    ]
    indexed_keywords = [[i + 1, item.keyword, item.count] for i, item in enumerate(keywords)]
    filled_data = data + indexed_keywords

    # Create a Table with the data
    t = Table(filled_data)

    # Add grid to the table
    table_style = TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])
    t.setStyle(table_style)

    # Add the table to elements
    elements.append(t)

    # Create text for paragraph 2 and add it to the elements
    paragraph_2_text = """
        Welcome to the histogram view of our data table. This
        visual representation shows the top 15 most used keywords
        from different news sites, ranked from the highest to the
        lowest number of hits.
    """

    paragraph2 = Paragraph(paragraph_2_text, paragraph_style)
    elements.append(paragraph2)

    # Create the bar data necessary for generation
    bar_data = [(item.keyword, item.count) for i, item in enumerate(keywords)]
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